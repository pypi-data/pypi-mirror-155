# ===============================================================================
# Copyright 2021 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import os

import click
import platform

from pcm.func import _login, _edm, _setupfiles, _code, _launcher, _init
from pcm.util import echo_config


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--template",
    default=None,
    help="Device Template to use. Typically the device models name",
)
@click.argument("name")
def device(template, name):
    click.echo("Create a new device configuration")


@cli.command()
@click.option(
    "--app",
    default="pycrunch",
    help="Application style to install. pycrunch, pyexperiment,...",
)
@click.option("--conda/--no-conda", default=False, help="Use Conda")
@click.option("--src/--no-src", "use_src", default=True, help="install the source code")
@click.option("--app_id", default=0, help="set the app id")
@click.option(
    "--fork", default="PychronLabsLLC", help="Name of the pychron fork to clone"
)
@click.option(
    "--org",
    default="NMGRL",
    help="Github organization for storing laboratory files such as Plot Options",
)
@click.option("--branch", default="dev/dr", help="Name of the pychron fork to clone")
@click.option(
    "--setupfiles/--no-setupfiles",
    "use_setupfiles",
    default=False,
    help="Install pychron setupfiles",
)
@click.option(
    "--init/--no-init",
    "use_init",
    default=True,
    help="Install pychron initalization files",
)
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option(
    "--edm/--no-edm", "use_edm", default=True, help="Install the EDM environment"
)
@click.option("--environment", default="pychron", help="Name of the EDM environment")
@click.option(
    "--launcher/--no-launcher",
    "use_launcher",
    default=True,
    help="make a launcher script",
)
@click.option("--app_id", default=0, help="set the app id")
@click.option(
    "--use_login/--no-use_login", default=True, help="Write default login files"
)
@click.option("--login/--no-login", default=0, help="show login window at startup")
@click.option(
    "--massspec_db_version", "msv", default=16, help="massspec database version"
)
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def wizard(
    app,
    conda,
    use_src,
    app_id,
    fork,
    org,
    branch,
    use_setupfiles,
    use_init,
    env,
    use_edm,
    environment,
    use_launcher,
    use_login,
    login,
    msv,
    overwrite,
    verbose,
):
    echo_config(
        app,
        conda,
        use_src,
        app_id,
        fork,
        org,
        branch,
        use_setupfiles,
        use_init,
        env,
        use_edm,
        environment,
        use_launcher,
        use_login,
        login,
        msv,
        overwrite,
        verbose,
    )
    click.secho("Install the pychron application", bold="True", fg="green")
    if use_src:
        _code(fork, branch, app_id)

    if use_init:
        _init(env, org, overwrite, verbose)

    if use_setupfiles:
        _setupfiles(env, overwrite, verbose)

    if use_edm:
        _edm(environment, app, verbose)

    if use_launcher:
        _launcher(
            conda, environment, app, fork, app_id, login, msv, None, overwrite, verbose
        )

    if use_login:
        _login(env, app_id)


@cli.command()
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option("--app_id", default=0, help="set the app id")
def login(env, app_id):
    _login(env, app_id)


@cli.command()
@click.option("--environment", default=None, help="Name of the EDM environment")
@click.option(
    "--app",
    default="pycrunch",
    help="Application style to install. pycrunch, pyexperiment,...",
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def edm(environment, app, verbose):
    _edm(environment, app, verbose)


@cli.command()
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def setupfiles(env, overwrite, verbose):
    _setupfiles(env, overwrite, verbose)


@cli.command()
@click.option("--fork", help="Name of the pychron fork to clone")
@click.option("--branch", default="dev/dr", help="Name of the pychron fork to clone")
@click.option("--app_id", default=0, help="set the app id")
def code(fork, branch, app_id):
    _code(fork, branch, app_id)


@cli.command()
@click.option("--conda/--no-conda", default=False, help="Use the conda package manager")
@click.option("--environment", default="pychron", help="Python environment name")
@click.option("--app", default="pycrunch", help="application name")
@click.option("--org", default="PychronLabsLLC", help="Github organization")
@click.option("--app_id", default=0, help="set the app id")
@click.option("--login/--no-login", default=0, help="show login window at startup")
@click.option(
    "--massspec_db_version", "msv", default=16, help="massspec database version"
)
@click.option("--output", default="pychron_launcher.sh", help="Output path")
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def launcher(
    conda, environment, app, org, app_id, login, msv, output, overwrite, verbose
):
    _launcher(
        conda, environment, app, org, app_id, login, msv, output, overwrite, verbose
    )


@cli.command()
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option(
    "--org",
    default="NMGRL",
    help="Github organization for storing laboratory files such as Plot Options",
)
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def init(env, org, overwrite, verbose):
    _init(env, org, overwrite, verbose)


if __name__ == "__main__":
    cli()
# ============= EOF =============================================
