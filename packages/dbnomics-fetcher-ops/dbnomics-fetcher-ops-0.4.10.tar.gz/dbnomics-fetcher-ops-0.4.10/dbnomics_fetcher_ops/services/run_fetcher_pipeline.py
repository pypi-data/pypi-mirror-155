"""Run fetcher pipeline, the application-level service."""

from typing import Optional, TypeAlias

import daiquiri
from gitlab.v4.objects import ProjectPipeline

from dbnomics_fetcher_ops.gitlab import init_gitlab_client
from dbnomics_fetcher_ops.model import FetcherMetadata
from dbnomics_fetcher_ops.utils import without_none_values

__all__ = ["run_fetcher_pipeline"]

logger = daiquiri.getLogger(__name__)


def run_fetcher_pipeline(
    provider_slug: str,
    *,
    debug_gitlab: bool = False,
    fetcher_metadata: FetcherMetadata,
    gitlab_private_token: str,
    json_data_from_git: bool = False,
    json_data_pipeline_id: Optional[int] = None,
    source_data_from_git: bool = False,
    source_data_pipeline_id: Optional[int] = None,
    start_from: Optional[str] = None,
) -> ProjectPipeline:
    # Create GitLab client.
    gitlab_url = fetcher_metadata.gitlab.base_url
    gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

    project_ref = fetcher_metadata.gitlab.fetcher
    fetcher_group_name, fetcher_project_name = project_ref.expand_group_and_name(provider_slug)
    project_path_with_namespace = f"{fetcher_group_name}/{fetcher_project_name}"

    fetcher_project = gl.projects.get(project_path_with_namespace)

    pipeline_variables = without_none_values(
        {
            "START_FROM": start_from,
            "SOURCE_DATA_PIPELINE_ID": source_data_pipeline_id,
            "JSON_DATA_PIPELINE_ID": json_data_pipeline_id,
            "SOURCE_DATA_FROM_GIT": source_data_from_git,
            "JSON_DATA_FROM_GIT": json_data_from_git,
        }
    )

    logger.debug(
        "About to run a pipeline for the project %r with variables %r...",
        fetcher_project.path_with_namespace,
        pipeline_variables,
    )

    pipeline = fetcher_project.pipelines.create(
        {"ref": fetcher_project.default_branch, "variables": to_key_value_pipeline_variables(pipeline_variables)}
    )
    logger.info("Created pipeline %r for project %r, see also %s", pipeline, fetcher_project, pipeline.web_url)


PipelineVariableValue: TypeAlias = int | str | bool | None


def to_key_value_pipeline_variable(value: PipelineVariableValue) -> str:
    """Convert a Python value to a string understood by GitLab CI as a pipeline variable value."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bool):
        return "1" if value else "0"
    raise TypeError(value)


def to_key_value_pipeline_variables(d: dict[str, PipelineVariableValue]) -> list[dict[str, str]]:
    """Convert a dict of Python values to a list of GitLab CI pipeline variables."""
    return [{"key": k, "value": to_key_value_pipeline_variable(v)} for k, v in d.items()]
