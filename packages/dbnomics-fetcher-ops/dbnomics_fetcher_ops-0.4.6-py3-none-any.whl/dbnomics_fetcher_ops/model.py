# dbnomics-fetcher-ops -- Manage DBnomics fetchers
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-fetcher-ops
#
# dbnomics-fetcher-ops is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-fetcher-ops is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Literal, Optional, Tuple, Union

from boltons.iterutils import first
from pydantic import BaseModel, Field, HttpUrl, validator

__all__ = [
    "FetcherDef",
    "FetcherDefNotFound",
    "FetcherMetadata",
    "GitLabStructure",
    "known_pipeline_versions",
    "PipelinesConfig",
    "PipelineV5Config",
    "PipelineVersion",
    "PipelineVersionError",
    "PipelineVersions",
    "ProjectRef",
    "ProviderCode",
    "ScheduleDef",
    "UnsupportedModelVersion",
    "validate_pipeline_version",
]

known_pipeline_versions = ["v1", "v2", "v5"]
PipelineVersion = Literal["v1", "v2", "v5"]

UpdateStrategy = Literal["merge", "replace"]


@dataclass
class FetcherDefNotFound(Exception):
    provider_slug: str

    def __str__(self) -> str:
        return f"Could not find fetcher definition for provider {self.provider_slug!r}"


@dataclass
class PipelineVersionError(Exception):
    version: str


@dataclass
class UnsupportedModelVersion(Exception):
    """fetchers.yml version is different from the one expected by the client."""

    expected: int
    found: int


def check_model_version(found: int, *, expected: int):
    if found != expected:
        raise UnsupportedModelVersion(expected=expected, found=found)


def validate_pipeline_version(version: str):
    if version not in known_pipeline_versions:
        raise PipelineVersionError(version=version)


class ScheduleDef(BaseModel):
    cron: str
    owner: str
    timezone: str


LabelValue = Union[str, int, float]

DownloadMode = Literal["full", "incremental"]

ProviderCode = str


class FetcherDef(BaseModel):
    """The definition of a fetcher.

    Pipeline versions are described in [this issue](https://git.nomics.world/dbnomics-fetchers/management/-/issues/948).
    """

    provider_code: ProviderCode
    provider_slug: str
    pipeline: PipelineVersion
    category_tree_update_strategy: UpdateStrategy = "merge"
    dataset_update_strategy: UpdateStrategy = "replace"
    download_mode: DownloadMode = "full"
    env: Dict[str, str] = Field(default_factory=dict)
    labels: Dict[str, LabelValue] = Field(default_factory=dict)
    schedules: List[ScheduleDef] = Field(default_factory=list)


class ProjectRef(BaseModel):
    group: str
    name: str
    env: Dict[str, str] = Field(default_factory=dict)
    fork_from: Optional[str] = None

    def expand(self, value: str, provider_slug: str) -> str:
        """Expand the provider slug in the given value."""
        variables = {"PROVIDER_SLUG": provider_slug}
        for k, v in variables.items():
            value = value.replace("{" + k + "}", v)
        return value

    def expand_group_and_name(self, provider_slug: str) -> Tuple[str, str]:
        """Return a tuple with the group name and project name resolved with the given provider slug."""
        return self.expand(self.group, provider_slug), self.expand(self.name, provider_slug)


class GitLabStructure(BaseModel):
    base_url: HttpUrl
    fetcher: ProjectRef
    json_data: ProjectRef
    source_data: ProjectRef

    @validator("base_url")
    def trim_end_slash(cls, v):
        return v.rstrip("/")

    def get_http_clone_url(self, provider_slug: str, *, project_ref: ProjectRef) -> str:
        group, name = project_ref.expand_group_and_name(provider_slug)
        return f"{self.base_url}/{group}/{name}.git"


class FetcherMetadata(BaseModel):
    version: int

    fetchers: List[FetcherDef]
    gitlab: GitLabStructure

    def find_fetcher_def_by_provider_slug(self, provider_slug: str) -> FetcherDef:
        """Find the FetcherDef item corresponding to the provider slug.

        Raise FetcherDefNotFound if not found.
        """
        for fetcher in self.fetchers:
            if fetcher.provider_slug == provider_slug:
                return fetcher
        raise FetcherDefNotFound(provider_slug=provider_slug)

    validator("version", allow_reuse=True)(partial(check_model_version, expected=2))


class FileDef(BaseModel):
    content: str
    if_exists: Literal["keep", "replace"]
    path: str


class PipelineV5ConfigFetcherProject(BaseModel):
    files: List[FileDef]

    def find_file(self, name: str) -> Optional[str]:
        return first(self.files, key=lambda file: file.name == name, default=None)


class PipelineV5Config(BaseModel):
    fetcher_project: PipelineV5ConfigFetcherProject


class PipelineVersions(BaseModel):
    v5: PipelineV5Config


class PipelinesConfig(BaseModel):
    version: int

    pipeline_versions: PipelineVersions

    validator("version", allow_reuse=True)(partial(check_model_version, expected=1))
