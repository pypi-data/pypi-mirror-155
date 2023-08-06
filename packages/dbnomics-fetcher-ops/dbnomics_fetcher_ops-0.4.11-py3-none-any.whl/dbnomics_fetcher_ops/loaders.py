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


from pathlib import Path

import daiquiri
import requests
import validators
from ruamel.yaml import YAML

from .model import FetcherMetadata, PipelinesConfig

__all__ = ["load_fetchers_yml", "load_pipelines_yml"]

logger = daiquiri.getLogger(__name__)

yaml = YAML(typ="safe")


def load_bytes(source: str) -> bytes:
    """Load ``source`` which can be a file path or an URL."""
    if validators.url(source):
        response = requests.get(source)
        response.raise_for_status()
        return response.content

    # Assume it is a file if it's not an URL.
    return Path(source).read_bytes()


def load_fetchers_yml(fetchers_yml_ref: str) -> FetcherMetadata:
    logger.debug("Loading fetcher metadata from %s...", fetchers_yml_ref)
    fetchers_yml_data = load_yml_file(fetchers_yml_ref)
    return FetcherMetadata.parse_obj(fetchers_yml_data)


def load_pipelines_yml(pipelines_yml_ref: str) -> PipelinesConfig:
    logger.debug("Loading pipelines config from %s...", pipelines_yml_ref)
    pipelines_yml_data = load_yml_file(pipelines_yml_ref)
    return PipelinesConfig.parse_obj(pipelines_yml_data)


def load_yml_file(ref: str):
    text = load_bytes(ref)
    return yaml.load(text)
