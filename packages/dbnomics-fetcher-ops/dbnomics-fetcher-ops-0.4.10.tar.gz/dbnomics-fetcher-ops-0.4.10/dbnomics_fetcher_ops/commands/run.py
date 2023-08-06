"""Run fetcher pipeline, the CLI command."""

from typing import Optional

import humanfriendly
import typer
from typer import Option

from dbnomics_fetcher_ops.services.run_fetcher_pipeline import run_fetcher_pipeline

__all__ = ["run_command"]


def run_command(
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
    gitlab_private_token: str = Option(..., envvar="GITLAB_PRIVATE_TOKEN"),
    json_data_from_git: bool = Option(False, envvar="JSON_DATA_FROM_GIT"),
    json_data_pipeline_id: Optional[int] = Option(None, envvar="JSON_DATA_PIPELINE_ID"),
    provider_slug: str = Option(..., envvar="PROVIDER_SLUG"),
    source_data_from_git: bool = Option(False, envvar="SOURCE_DATA_FROM_GIT"),
    source_data_pipeline_id: Optional[int] = Option(None, envvar="SOURCE_DATA_PIPELINE_ID"),
    start_from: Optional[str] = Option(None, envvar="START_FROM"),
):
    """Run a pipeline for a fetcher, with options."""
    from ..app_args import app_args

    assert app_args is not None

    run_fetcher_pipeline(
        provider_slug,
        debug_gitlab=debug_gitlab,
        fetcher_metadata=app_args.fetcher_metadata,
        gitlab_private_token=gitlab_private_token,
        json_data_from_git=json_data_from_git,
        json_data_pipeline_id=json_data_pipeline_id,
        source_data_from_git=source_data_from_git,
        source_data_pipeline_id=source_data_pipeline_id,
        start_from=start_from,
    )


def parse_time_span(value: str) -> int:
    """Parse the value representing a time span.

    The value must respect the "human friendly" format.
    If it's a bare number (without any unit), it will be interpreted as seconds.

    Cf https://humanfriendly.readthedocs.io/en/latest/api.html#humanfriendly.parse_timespan

    Return the duration in seconds as an integer value.
    """
    try:
        return humanfriendly.parse_timespan(value)
    except humanfriendly.InvalidTimespan:
        doc_url = "https://humanfriendly.readthedocs.io/en/latest/api.html#humanfriendly.parse_timespan"
        typer.echo(f"Invalid value for the --min-duration option: {value!r}, cf {doc_url}")
        raise typer.Abort()
