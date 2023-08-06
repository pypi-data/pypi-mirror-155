#! /usr/bin/env python3

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

"""CLI to manage DBnomics fetchers."""


import logging

import daiquiri
import typer
from dotenv import load_dotenv
from xdg import xdg_config_home

from . import app_args, loaders
from .commands.apply import apply_command
from .commands.configure import configure_command
from .commands.list import list_command
from .commands.run import run_command
from .commands.undeploy import undeploy_command

# Do this before calling os.getenv().
config_env_file = xdg_config_home() / "dbnomics" / "dbnomics-fetchers.env"
load_dotenv(config_env_file)
load_dotenv()

logger = daiquiri.getLogger(__name__)

app = typer.Typer()
app.command(name="apply")(apply_command)
app.command(name="configure")(configure_command)
app.command(name="list")(list_command)
app.command(name="run")(run_command)
app.command(name="undeploy")(undeploy_command)


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def callback(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "-d", "--debug", envvar="DEBUG", help="Display DEBUG log messages"),
    dry_run: bool = typer.Option(False, "-n", "--dry-run", envvar="DRY_RUN", help="Do not execute actions for real"),
    verbose: bool = typer.Option(False, "-v", "--verbose", envvar="VERBOSE", help="Display INFO log messages"),
    fetchers_yml: str = typer.Option(..., envvar="FETCHERS_YML", help="Path or URL to fetchers.yml"),
    pipelines_yml: str = typer.Option(..., envvar="PIPELINES_YML", help="Path or URL to pipelines.yml"),
):
    """Manage DBnomics fetchers."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [(__package__, logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )

    fetcher_metadata = loaders.load_fetchers_yml(fetchers_yml)
    pipelines_config = loaders.load_pipelines_yml(pipelines_yml)

    app_args.app_args = app_args.AppArgs(
        debug=debug,
        dry_run=dry_run,
        fetcher_metadata=fetcher_metadata,
        fetchers_yml=fetchers_yml,
        pipelines_config=pipelines_config,
        pipelines_yml=pipelines_yml,
        verbose=verbose,
    )


def main():
    app()


if __name__ == "__main__":
    main()
