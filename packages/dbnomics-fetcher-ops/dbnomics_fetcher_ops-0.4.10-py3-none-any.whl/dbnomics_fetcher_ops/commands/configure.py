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


import base64
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, timedelta
from time import sleep
from typing import Optional

import daiquiri
import gitlab
import typer
from gitlab.v4.objects import VISIBILITY_PUBLIC, DeployKey, Project, ProjectPipelineSchedule, User
from gitlab.v4.objects.variables import Variable

from ..app_args import check_provider_slug_is_lowercase, get_fetcher_def_not_found_error_message
from ..gitlab import init_gitlab_client
from ..model import FetcherDef, FetcherDefNotFound, FetcherMetadata, FileDef, PipelineV5Config, ScheduleDef
from ..ssh import generate_ssh_key_pair
from ..utils import find_index

logger = daiquiri.getLogger(__name__)

CI_JOBS_KEY = "CI jobs"
DEFAULT_BRANCH = "master"
SSH_PRIVATE_KEY = "SSH_PRIVATE_KEY"

DBNOMICS_NAMESPACE = "dbnomics"
DBNOMICS_DATA_MODEL = "dbnomics-data-model"
DBNOMICS_SOLR = "dbnomics-solr"


def configure_command(
    provider_slug: str = typer.Argument(..., callback=check_provider_slug_is_lowercase),
    gitlab_private_token: str = typer.Option(
        ..., envvar="GITLAB_PRIVATE_TOKEN", help="Private access token used to authenticate to GitLab API"
    ),
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
):
    """Configure a fetcher."""
    # Defer import to let the cli.callback function write the variable and avoid importing None.
    from ..app_args import app_args

    assert app_args is not None

    try:
        fetcher_def = app_args.fetcher_metadata.find_fetcher_def_by_provider_slug(provider_slug)
    except FetcherDefNotFound:
        logger.error(get_fetcher_def_not_found_error_message(provider_slug, app_args.fetchers_yml))
        raise typer.Abort()

    pipeline_v5_config = app_args.pipelines_config.pipeline_versions.v5

    try:
        configure_fetcher(
            fetcher_def,
            debug_gitlab=debug_gitlab,
            fetcher_metadata=app_args.fetcher_metadata,
            gitlab_private_token=gitlab_private_token,
            pipeline_v5_config=pipeline_v5_config,
        )
    except UnsupportedPipelineVersion as exc:
        logger.warning(
            "Fetcher %r uses an unsupported pipeline version %r in fetchers.yml, skipping", provider_slug, exc.version
        )


def configure_fetcher(
    fetcher_def: FetcherDef,
    *,
    debug_gitlab: bool,
    fetcher_metadata: FetcherMetadata,
    gitlab_private_token: str,
    pipeline_v5_config: PipelineV5Config,
):
    """Configure a fetcher.

    Called from apply and configure CLI commands.

    Configures GitLab projects of fetcher, json-data and source-data.

    Supports only pipeline v5.

    Cleanups elements from pipelines v1 or v2.
    """
    if fetcher_def.pipeline != "v5":
        raise UnsupportedPipelineVersion(version=fetcher_def.pipeline)

    # Create GitLab client.
    gitlab_url = fetcher_metadata.gitlab.base_url
    gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

    ctx = Context(debug_gitlab=debug_gitlab, gitlab_url=gitlab_url, gl=gl, provider_slug=fetcher_def.provider_slug)

    fetcher_project = init_fetcher_project(gl, fetcher_metadata, ctx)
    source_data_project = load_or_create_source_data_project(gl, fetcher_metadata, ctx)
    json_data_project = load_or_create_json_data_project(gl, fetcher_metadata, ctx)

    # Setup CI conf.
    write_fetcher_project_files(fetcher_project, pipeline_v5_config)
    setup_pipeline_variables(fetcher_project, source_data_project, json_data_project, fetcher_def, fetcher_metadata)
    setup_pipeline_schedules(fetcher_project, fetcher_def, ctx)
    ensure_ssh_key_pairs(fetcher_project, source_data_project, json_data_project, ctx)

    cleanup_elements_from_previous_pipeline_versions(fetcher_project, source_data_project, json_data_project, ctx)


@dataclass
class UnsupportedPipelineVersion(Exception):
    version: str


@dataclass
class TakeOwnershipError(Exception):
    new_owner_name: str
    schedule: ProjectPipelineSchedule

    details: Optional[str] = None

    def __str__(self):
        message = f"User {self.new_owner_name!r} could not take ownership of schedule {self.schedule!r}."
        if self.details is not None:
            message += f" {self.details}"
        return message


@dataclass
class Context:
    debug_gitlab: bool
    gitlab_url: str
    gl: gitlab.Gitlab
    provider_slug: str


def cleanup_elements_from_previous_pipeline_versions(
    fetcher_project: Project,
    source_data_project: Project,
    json_data_project: Project,
    ctx: Context,
) -> None:
    """Cleanup elements from pipelines v1 or v2.

    This includes webhooks of source-data and json-data project.
    """
    gl = ctx.gl
    data_model_project = gl.projects.get(f"{DBNOMICS_NAMESPACE}/{DBNOMICS_DATA_MODEL}")
    solr_project = gl.projects.get(f"{DBNOMICS_NAMESPACE}/{DBNOMICS_SOLR}")

    cleanup_source_data_webhooks_from_previous_pipeline_versions(source_data_project, fetcher_project)
    cleanup_json_data_webhooks_from_previous_pipeline_versions(json_data_project, data_model_project, solr_project)


def cleanup_json_data_webhooks_from_previous_pipeline_versions(
    json_data_project: Project, data_model_project: Project, solr_project: Project
) -> None:
    """Cleanup webhooks of a json-data project defined by pipelines v1 or v2.

    This includes:

    - the webhook that triggers a data model validation,
    - the webhook that triggers a Solr indexation.
    """
    url_prefix_template = "https://git.nomics.world/api/v4/projects/{project_id}/ref/master/trigger/pipeline"
    data_model_url_prefix = url_prefix_template.format(project_id=data_model_project.id)
    solr_url_prefix = url_prefix_template.format(project_id=solr_project.id)

    for hook in json_data_project.hooks.list(as_list=False):
        # Check if hook triggers a data model validation.
        if hook.url.startswith(data_model_url_prefix):
            logger.info(
                "Deleting hook %r that triggers a data model validation in a previous version of the pipeline", hook
            )
            hook.delete()

        # Check if hook triggers an indexation.
        elif hook.url.startswith(solr_url_prefix):
            logger.info("Deleting hook %r that triggers a Solr indexation in a previous version of the pipeline", hook)
            hook.delete()


def cleanup_source_data_webhooks_from_previous_pipeline_versions(
    source_data_project: Project, fetcher_project: Project
) -> None:
    """Cleanup webhooks of a source-data project defined by pipelines v1 or v2.

    This includes the webhook that triggers a convert job.
    """
    url_prefix_template = "https://git.nomics.world/api/v4/projects/{project_id}/ref/master/trigger/pipeline"
    fetcher_url_prefix = url_prefix_template.format(project_id=fetcher_project.id)

    for hook in source_data_project.hooks.list(as_list=False):
        # Check if hook triggers a convert job.
        if hook.url.startswith(fetcher_url_prefix):
            logger.info("Deleting hook %r that triggers a convert script in a previous version of the pipeline", hook)
            hook.delete()


def init_fetcher_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, ctx: Context) -> Project:
    """Load or fork or create fetcher project."""
    project_ref = fetcher_metadata.gitlab.fetcher
    fetcher_group_name, fetcher_project_name = project_ref.expand_group_and_name(ctx.provider_slug)
    project_path_with_namespace = f"{fetcher_group_name}/{fetcher_project_name}"
    try:
        return gl.projects.get(project_path_with_namespace)
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise

    fork_from_raw = project_ref.fork_from
    if fork_from_raw is not None:
        fork_from = project_ref.expand(fork_from_raw, ctx.provider_slug)
        logger.debug("Fetcher project does not exist, forking from %r...", fork_from)
        try:
            upstream_project = gl.projects.get(fork_from)
        except gitlab.exceptions.GitlabGetError as exc:
            if exc.response_code != 404:
                raise
            logger.error("Could not find project %r, skipping fork and creating new project", fork_from)
        else:
            return fork_project(upstream_project, fetcher_group_name, fetcher_project_name, ctx)

    logger.debug("Fetcher project does not exist, creating...")
    fetcher_description = f"Source code of the fetcher for provider {ctx.provider_slug}"
    return create_project(fetcher_group_name, fetcher_project_name, fetcher_description, ctx)


def load_or_create_source_data_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, ctx: Context) -> Project:
    source_data_group_name, source_data_project_name = fetcher_metadata.gitlab.source_data.expand_group_and_name(
        ctx.provider_slug
    )
    try:
        return gl.projects.get(f"{source_data_group_name}/{source_data_project_name}")
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
    logger.debug("Source data project does not exist, creating...")
    source_data_description = f"Source data as downloaded from provider {ctx.provider_slug}"
    return create_project(source_data_group_name, source_data_project_name, source_data_description, ctx)


def load_or_create_json_data_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, ctx: Context) -> Project:
    json_data_group_name, json_data_project_name = fetcher_metadata.gitlab.json_data.expand_group_and_name(
        ctx.provider_slug
    )
    try:
        return gl.projects.get(f"{json_data_group_name}/{json_data_project_name}")
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
    logger.debug("JSON data project does not exist, creating...")
    json_data_description = "Data following DBnomics data model, converted from provider data"
    return create_project(json_data_group_name, json_data_project_name, json_data_description, ctx)


def get_deploy_key_title(ctx: Context):
    return f"{ctx.provider_slug} {CI_JOBS_KEY}"


def find_variable_by_name(project: Project, name: str) -> Optional[Variable]:
    try:
        return project.variables.get(name)
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
        return None


def find_deploy_key_by_title(ctx: Context, title: str) -> Optional[DeployKey]:
    for key in ctx.gl.deploykeys.list(as_list=False):
        if key.title == title:
            assert isinstance(key, DeployKey), key
            return key
    return None


def find_project_deploy_key_by_title(project: Project, title: str) -> Optional[DeployKey]:
    for key in project.keys.list(as_list=False):
        if key.title == title:
            return key
    return None


def delete_env_variable(project: Project, name: str, ctx: Context):
    logger.debug("Deleting environment variable %r of %r...", name, project.path_with_namespace)
    try:
        variable = project.variables.get(name)
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
        logger.debug("Environment variable %r was not found in %r", name, project.path_with_namespace)
        return
    variable.delete()
    logger.info("Environment variable %r was deleted from %r", variable, project.path_with_namespace)


def delete_deploy_keys(project: Project, ctx: Context):
    logger.debug("Deleting deploy keys of %r...", project.path_with_namespace)
    for key in project.keys.list(as_list=False):
        if key.title != get_deploy_key_title(ctx):
            logger.warning("%r ignored, title: %r", key, key.title)
            continue
        key.delete()
        logger.info("%r deleted from %r", key, project.path_with_namespace)
    else:
        logger.debug("No deploy key found for %r", project.path_with_namespace)


def ensure_ssh_key_pairs(
    fetcher_project: Project,
    source_data_project: Project,
    json_data_project: Project,
    ctx: Context,
):
    """Checks that the SSH key pairs are configured, otherwise configure them.

    In particular ensure that the fetcher project has a SSH_PRIVATE_KEY masked variable,
    and that source-data and json-data projects have a deploy key.
    """
    ssh_private_key_variable = find_variable_by_name(fetcher_project, SSH_PRIVATE_KEY)
    deploy_key_title = get_deploy_key_title(ctx)
    source_data_deploy_key = find_project_deploy_key_by_title(source_data_project, deploy_key_title)
    json_data_deploy_key = find_project_deploy_key_by_title(json_data_project, deploy_key_title)
    if not ssh_private_key_variable or not source_data_deploy_key or not json_data_deploy_key:
        # Do some cleanup.
        delete_env_variable(fetcher_project, SSH_PRIVATE_KEY, ctx)
        delete_deploy_keys(source_data_project, ctx)
        delete_deploy_keys(json_data_project, ctx)

        # Generate a new SSH key pair, set private key to a fetcher project variable,
        # and create a deploy key from SSH public key used by both source-data
        # and json-data projects.
        ssh_public_key, ssh_private_key = generate_ssh_key_pair(ctx.provider_slug)
        fetcher_project.variables.create({"key": SSH_PRIVATE_KEY, "value": ssh_private_key})
        # Do not display private key value.
        logger.info("%r added to %r", SSH_PRIVATE_KEY, fetcher_project.path_with_namespace)
        deploy_key = source_data_project.keys.create(
            {"title": deploy_key_title, "key": ssh_public_key, "can_push": True}
        )
        logger.info("%r enabled for %r", deploy_key, source_data_project.path_with_namespace)
        json_data_project.keys.enable(deploy_key.id)
        json_data_project.keys.update(deploy_key.id, {"can_push": True})
        logger.info("%r enabled for %r", deploy_key, json_data_project.path_with_namespace)
    else:
        logger.debug("SSH key pair is already configured for this fetcher")


def setup_pipeline_variables(
    fetcher_project: Project,
    source_data_project: Project,
    json_data_project: Project,
    fetcher_def: FetcherDef,
    fetcher_metadata: FetcherMetadata,
):
    """Setup pipeline variables in CI settings.

    Some variables are computed, some other are taken from the fetcher project metadata in fetchers.yml.
    """
    computed_variables = {
        "CATEGORY_TREE_UPDATE_STRATEGY": fetcher_def.category_tree_update_strategy,
        "DATASET_UPDATE_STRATEGY": fetcher_def.dataset_update_strategy,
        "DOWNLOAD_MODE": fetcher_def.download_mode,
        "JSON_DATA_REMOTE_SSH_URL": json_data_project.ssh_url_to_repo,
        "PROVIDER_SLUG": fetcher_def.provider_slug,
        "SOURCE_DATA_REMOTE_SSH_URL": source_data_project.ssh_url_to_repo,
    }
    variables = {**fetcher_metadata.gitlab.fetcher.env, **fetcher_def.env, **computed_variables}
    create_or_update_pipeline_variables(fetcher_project, variables)


def write_fetcher_project_files(fetcher_project: Project, pipeline_v5_config: PipelineV5Config):
    """Write fetcher project files defined in pipeline configuration.

    In particular: .gitlab-ci.yml and Dockerfile.

    If the file exists, follow "if_exists" policy (keep or replace).
    """
    for file_def in pipeline_v5_config.fetcher_project.files:
        write_fetcher_project_file(fetcher_project, file_def)


def write_fetcher_project_file(fetcher_project: Project, file_def: FileDef):
    """Write fetcher project file defined in pipeline configuration.

    If the file exists, follow "if_exists" policy (keep or replace).
    """
    try:
        project_file = fetcher_project.files.get(
            file_path=file_def.path, ref=fetcher_project.default_branch or DEFAULT_BRANCH
        )
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise

        # File does not exist, create it

        logger.debug("%r not found, adding it to project %r...", file_def.path, fetcher_project.path_with_namespace)
        project_file = fetcher_project.files.create(
            {
                "file_path": file_def.path,
                "branch": fetcher_project.default_branch or DEFAULT_BRANCH,
                "content": file_def.content,
                "author_email": "dbnomics-fetcher-ops@localhost",
                "author_name": "dbnomics-fetcher-ops",
                "commit_message": f"Add {file_def.path} from template found in pipeline configuration YAML file",
            }
        )
        logger.info("%r file %r created in %r", file_def.path, project_file, fetcher_project.path_with_namespace)
    else:
        # File already exists, apply "if_exists" policy

        if file_def.if_exists == "keep":
            logger.debug(
                "%r file %r already exists in %r, keeping it as-is",
                file_def.path,
                project_file,
                fetcher_project.path_with_namespace,
            )
            return

        elif file_def.if_exists == "replace":
            # Replace file if its content has changed
            # Note: although Git ignores empty commits, GitLab API can create some, so we have to check for changes.

            project_file_content = base64.b64decode(project_file.content).decode()
            if project_file_content.strip() == file_def.content.strip():
                logger.debug(
                    "%r found in project %r and content is up to date, doing nothing",
                    file_def.path,
                    fetcher_project.path_with_namespace,
                )
            else:
                logger.debug(
                    "%r found in project %r and content is not up to date, replacing content...",
                    file_def.path,
                    fetcher_project.path_with_namespace,
                )
                project_file.content = file_def.content
                project_file.save(
                    branch=fetcher_project.default_branch or DEFAULT_BRANCH,
                    commit_message=f"Replace {file_def.path} with template found in pipeline configuration YAML file",
                )
                logger.info(
                    "%r file %r updated in %r", file_def.path, project_file, fetcher_project.path_with_namespace
                )

        else:
            raise ValueError(f"Unsupported value for if_exists: {file_def.if_exists}")


def create_or_update_pipeline_variables(fetcher_project: Project, variables: dict):
    """Create or update pipeline variables for the fetcher project in CI settings."""
    for k, v in variables.items():
        variable = find_variable_by_name(fetcher_project, k)
        if variable is None:
            logger.debug("Variable %r was not found, creating it...", k)
            fetcher_project.variables.create({"key": k, "value": v})
            logger.info("Variable %r created", k)
        else:
            is_dirty = False
            if variable.value != v:
                variable.value = v
                is_dirty = True
            if is_dirty:
                logger.debug("Variable %r was found but is not up to date, updating it...", k)
                variable.save()
                logger.info("Variable %r updated", k)
            else:
                logger.debug("Variable %r was found and is up to date, doing nothing", k)


def create_pipeline_schedule(project: Project, schedule_def: ScheduleDef, ctx: Context) -> ProjectPipelineSchedule:
    schedule = project.pipelineschedules.create(
        {
            "active": True,
            "description": "Run fetcher",
            "ref": project.default_branch or DEFAULT_BRANCH,
            "cron": schedule_def.cron,
            "cron_timezone": schedule_def.timezone,
        }
    )
    take_ownership(schedule, schedule_def.owner, ctx)
    logger.info("%r created for %r with owner %r", schedule, project.path_with_namespace, schedule_def.owner)
    return schedule


def take_ownership(schedule: ProjectPipelineSchedule, owner_name: str, ctx: Context):
    gl = ctx.gl
    owners = gl.users.list(search=owner_name)
    if len(owners) == 0:
        raise TakeOwnershipError(new_owner_name=owner_name, schedule=schedule, details="User not found")

    assert isinstance(owners, list) and len(owners) == 1, owners
    owner = owners[0]
    assert isinstance(owner, User), owner

    with create_impersonation_token(
        owner,
        {
            "name": "dbnomics-fetcher-ops",
            "scopes": ["api"],
            "expires_at": (date.today() + timedelta(days=1)).isoformat(),
        },
    ) as owner_impersonation_token:
        gl2 = init_gitlab_client(
            ctx.gitlab_url, enable_debug=ctx.debug_gitlab, private_token=owner_impersonation_token.token
        )
        fetcher_project2 = gl2.projects.get(schedule.project_id)
        schedule2 = fetcher_project2.pipelineschedules.get(schedule.id)
        try:
            schedule2.take_ownership()
        except gitlab.exceptions.GitlabOwnershipError as exc:
            details = None
            if exc.response_code == 403:
                details = 'Forbidden. Hint: add that user to the members of the group with a "maintainer" role.'
            raise TakeOwnershipError(new_owner_name=owner_name, schedule=schedule, details=details) from exc


@contextmanager
def create_impersonation_token(user: User, token_params):
    impersonation_token = user.impersonationtokens.create(token_params)
    try:
        yield impersonation_token
    finally:
        impersonation_token.delete()


def setup_pipeline_schedules(project: Project, fetcher_def: FetcherDef, ctx: Context):
    """Setup pipeline schedules to match exactly the ones defined in fetcher definition.

    Schedules that are not mentioned in fetcher definition are deleted.
    """
    logger.debug("Configuring pipeline schedules for project %r...", project.path_with_namespace)

    schedule_defs = fetcher_def.schedules.copy()

    for schedule in project.pipelineschedules.list(as_list=False):
        schedule_def_index = find_index(
            lambda schedule_def: schedule_def.cron == schedule.cron and schedule_def.timezone == schedule.cron_timezone,
            schedule_defs,
            default=None,
        )
        if schedule_def_index is None:
            logger.info("Deleting schedule %r that is not mentioned in fetcher definition...", schedule)
            schedule.delete()
        else:
            schedule_def = schedule_defs.pop(schedule_def_index)
            if schedule.owner["username"] != schedule_def.owner:
                logger.info(
                    "Owner of existing schedule %r is different from %r, taking ownership...", schedule, schedule_def
                )
                take_ownership(schedule, schedule_def.owner, ctx)

    for schedule_def in schedule_defs:
        logger.info("Creating schedule from %r...", schedule_def)
        create_pipeline_schedule(project, schedule_def, ctx)


def create_project(group_name: str, project_name: str, description: str, ctx: Context):
    group = load_or_create_group(group_name, ctx)
    project = ctx.gl.projects.create(
        {"name": project_name, "namespace_id": group.id, "description": description, "visibility": VISIBILITY_PUBLIC}
    )
    logger.info("Project created: %r", project.path_with_namespace)
    return project


def create_group(group_name: str, ctx: Context):
    gl = ctx.gl
    parent_group_name, _, group_name = group_name.rpartition("/")
    parent_group_id = None
    if parent_group_name:
        parent_group = gl.groups.get(parent_group_name)
        parent_group_id = parent_group.id
    group = gl.groups.create({"name": group_name, "path": group_name, "parent_id": parent_group_id})
    logger.info("Group created: %r", f"{parent_group_name}/{group.path}")
    return group


def load_or_create_group(group_name: str, ctx: Context):
    try:
        return ctx.gl.groups.get(group_name)
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
    logger.debug("Group %r not found, creating...", group_name)
    return create_group(group_name, ctx)


def fork_project(upstream_project: Project, group_name: str, project_name: str, ctx: Context) -> Project:
    """Fork a project.

    Wait for the fork to really happen, it can take several seconds.
    The more pragmatic way to check if the fork was done is to wait for commits to appear.

    Return a Project instance, not a ProjectFork.
    """
    group = load_or_create_group(group_name, ctx)
    project_fork = upstream_project.forks.create({"namespace_id": group.id, "path": project_name})
    project = ctx.gl.projects.get(project_fork.id)
    commits = []
    while True:
        try:
            commits = project.commits.list(per_page=1)
        except gitlab.exceptions.GitlabListError:
            # GitLab can return a 500 error when fetching commits while forking.
            pass
        if commits:
            break
        sleep(1)
    logger.info("Forked project %r from %r", project.path_with_namespace, upstream_project.path_with_namespace)
    return project
