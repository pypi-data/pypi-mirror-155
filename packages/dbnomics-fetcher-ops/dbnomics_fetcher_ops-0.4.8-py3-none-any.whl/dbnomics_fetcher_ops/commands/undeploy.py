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


import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import gitlab
import typer
from dbnomics_solr import DBnomicsSolrClient
from dbnomics_solr.dbnomics_solr_client import ProviderNotFound
from gitlab.v4.objects import Project

from ..app_args import check_provider_slug_is_lowercase, get_fetcher_def_not_found_error_message
from ..gitlab import init_gitlab_client
from ..model import FetcherDefNotFound, FetcherMetadata

logger = logging.getLogger(__name__)


def undeploy_command(
    provider_slug: str = typer.Argument(..., callback=check_provider_slug_is_lowercase),
    git_repositories_root_dir: Optional[Path] = typer.Option(
        None,
        envvar="GIT_REPOSITORIES_ROOT_DIR",
        help="Directory where the fetcher pipeline keeps clones of the source-data and json-data Git repositories",
    ),
    gitlab_private_token: str = typer.Option(
        ..., envvar="GITLAB_PRIVATE_TOKEN", help="Private access token used to authenticate to GitLab API"
    ),
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
    solr_url: Optional[str] = typer.Option(None, envvar="SOLR_URL"),
    workspaces_root_dir: Optional[Path] = typer.Option(
        None,
        envvar="WORKSPACES_ROOT_DIR",
        help="Directory where the fetcher pipeline writes data to, during download and convert jobs",
    ),
):
    """Remove data of this provider on a DBnomics instance.

    This command:

    - disables the schedules of the GitLab project of the fetcher
    - deletes all the Solr documents corresponding to this provider
    - deletes the directories used by the fetcher pipeline (source-data and json-data clones, and workspace)

    As a consequence, the provider won't appear on DBnomics website and API anymore.

    This command does not delete:

    - the GitLab project of the source code of the fetcher
    - the GitLab project of "source-data"
    - the GitLab project of "json-data"
    - the "json-data" directory served by the API (this is done by dbnomics-sync-git)
    """
    # Defer import to let the cli.callback function write the variable and avoid importing None.
    from ..app_args import app_args

    assert app_args is not None

    try:
        undeploy_fetcher(
            provider_slug,
            debug_gitlab=debug_gitlab,
            fetcher_metadata=app_args.fetcher_metadata,
            git_repositories_root_dir=git_repositories_root_dir,
            gitlab_private_token=gitlab_private_token,
            solr_url=solr_url,
            workspaces_root_dir=workspaces_root_dir,
        )
    except FetcherDefNotFound:
        logger.error(get_fetcher_def_not_found_error_message(provider_slug, app_args.fetchers_yml))
        raise typer.Abort()


def undeploy_fetcher(
    provider_slug: str,
    *,
    debug_gitlab: bool,
    fetcher_metadata: FetcherMetadata,
    git_repositories_root_dir: Optional[Path],
    gitlab_private_token: str,
    solr_url: Optional[str],
    workspaces_root_dir: Optional[Path],
):
    # Disable GitLab schedules
    disable_schedules(
        provider_slug,
        debug_gitlab=debug_gitlab,
        fetcher_metadata=fetcher_metadata,
        gitlab_private_token=gitlab_private_token,
    )

    # Delete documents from Solr
    if solr_url is not None:
        delete_provider_from_solr(provider_slug, solr_url=solr_url)

    # Delete directories used by the fetcher pipeline
    delete_pipeline_directories(
        provider_slug, git_repositories_root_dir=git_repositories_root_dir, workspaces_root_dir=workspaces_root_dir
    )


def delete_pipeline_directories(
    provider_slug: str, *, git_repositories_root_dir: Optional[Path], workspaces_root_dir: Optional[Path]
):
    if git_repositories_root_dir is not None:
        git_repositories_dir = git_repositories_root_dir / provider_slug
        delete_pipeline_directory(git_repositories_dir)

    if workspaces_root_dir is not None:
        workspace_dir = workspaces_root_dir / provider_slug
        delete_pipeline_directory(workspace_dir)


def delete_pipeline_directory(path: Path):
    if path.is_dir():
        logger.info("Deleting pipeline directory: %r...", str(path))
        shutil.rmtree(path)


def delete_provider_from_solr(provider_slug: str, *, solr_url: str):
    logger.debug("Deleting documents related to provider %r from Solr...", provider_slug)
    dbnomics_solr_client = DBnomicsSolrClient(solr_url)
    try:
        dbnomics_solr_client.delete_by_provider_slug(provider_slug)
    except ProviderNotFound:
        logger.debug("Provider %r (slug) was not found in Solr index, skipping", provider_slug)


def disable_schedules(
    provider_slug: str, *, gitlab_private_token: str, debug_gitlab: bool, fetcher_metadata: FetcherMetadata,
):
    logger.debug("Disabling schedules of fetcher %r...", provider_slug)

    # Create GitLab client.
    gitlab_url = fetcher_metadata.gitlab.base_url
    gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

    try:
        fetcher_project = load_fetcher_project(gl, fetcher_metadata, provider_slug)
    except GitLabProjectNotFound as exc:
        logger.debug(
            "Could not find project %r for fetcher source code of provider %r, skipping disabling schedules",
            exc.project_path_with_namespace,
            provider_slug,
        )
        return

    for schedule in fetcher_project.pipelineschedules.list(as_list=False):
        logger.info("Deleting schedule %r for project %r", schedule, fetcher_project.path_with_namespace)
        schedule.delete()


@dataclass
class GitLabProjectNotFound(Exception):
    project_path_with_namespace: str


def load_fetcher_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, provider_slug: str) -> Project:
    fetcher_group_name, fetcher_project_name = fetcher_metadata.gitlab.fetcher.expand_group_and_name(provider_slug)
    project_path_with_namespace = f"{fetcher_group_name}/{fetcher_project_name}"
    try:
        fetcher_project = gl.projects.get(project_path_with_namespace)
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
        raise GitLabProjectNotFound(project_path_with_namespace=project_path_with_namespace) from exc
    return fetcher_project
