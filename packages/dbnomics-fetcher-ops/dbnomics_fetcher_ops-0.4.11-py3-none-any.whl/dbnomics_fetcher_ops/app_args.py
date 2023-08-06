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
from typing import Optional

import typer

from .model import FetcherMetadata, PipelinesConfig

__all__ = ["app_args", "AppArgs", "check_provider_slug_is_lowercase", "get_fetcher_def_not_found_error_message"]

app_args: Optional["AppArgs"] = None


@dataclass
class AppArgs:
    """Script arguments common to all commands."""

    fetcher_metadata: FetcherMetadata
    fetchers_yml: str
    pipelines_config: PipelinesConfig
    pipelines_yml: str

    debug: bool = False
    dry_run: bool = False
    verbose: bool = False


def check_provider_slug_is_lowercase(value: str):
    if value != value.lower():
        raise typer.BadParameter("Provider slug must be lowercase")
    return value


def get_fetcher_def_not_found_error_message(provider_slug: str, fetchers_yml: str) -> str:
    return f"Could not find fetcher definition for provider {provider_slug!r} in {fetchers_yml!r}"
