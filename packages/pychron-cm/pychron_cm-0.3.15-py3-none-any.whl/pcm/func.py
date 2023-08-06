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
import shutil
import subprocess
import platform

import click
import yaml

from pcm import util, requirements, render

IS_MAC = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"
HOME = os.path.expanduser("~")
EDM_ENVS_ROOT = os.path.join(HOME, ".edm", "envs")
EDM_BIN = os.path.join(EDM_ENVS_ROOT, "edm", "bin")

if IS_WINDOWS:
    GIT = "C:\\Git\\bin\\git"
else:
    GIT = "git"


def _login(env, app_id):
    # write the user
    root = os.path.join(HOME, f".pychron.{app_id}")
    user_file = os.path.join(root, "users.yaml")
    t = {
        "users": [
            "root",
        ],
        "last_login": "root",
    }
    util.write(user_file, yaml.dump(t))

    environment_file = os.path.join(root, "environments.yaml")
    pe = os.path.join(HOME, env)
    t = {
        "env": pe,
        "envs": [
            pe,
        ],
    }
    util.write(environment_file, yaml.dump(t))


def _edm(environment, app, verbose):
    click.secho("edm install", bold=True, fg="green")
    req = requirements.EDM_REQUIREMENTS
    pip_req = ["uncertainties", "qimage2ndarray", "pymysql"]

    if app == "pyvalve":
        req.extend(["pyserial", "twisted"])
    else:
        pip_req.extend(["peakutils", "utm"])

    cmdargs = ["edm", "install", "-y"] + req
    active_python = os.path.join(HOME, ".edm")
    if environment:
        active_python = os.path.join(
            active_python, "envs", environment, "bin", "python"
        )
        cmdargs.extend(["--environment", environment])
    else:
        active_python = os.path.join(active_python, "bin", "python")

    if verbose:
        click.echo(f'requirements: {" ".join(req)}')
        click.echo(f'command: {" ".join(cmdargs)}')

    subprocess.call(cmdargs)
    subprocess.call(
        [
            active_python,
            "-m",
            "pip",
            "install",
            "--no-dependencies",
        ]
        + pip_req
    )


def _setupfiles(env, overwrite, verbose):
    root = os.path.join(HOME, env)

    util.make_dir(root, "setupfiles")

    sf = os.path.join(root, "setupfiles")

    scripts = "scripts"
    util.make_dir(root, scripts)
    p = os.path.join(root, scripts, "defaults.yaml")
    util.write(p, render.render_template("defaults.yaml"), overwrite)

    measurement_args = "measurement", "unknown"
    extraction_args = "extraction", "extraction"
    procedure_args = "procedures", "procedure"

    for name, filename in (measurement_args, extraction_args, procedure_args):
        txt = render.render_template(filename)
        d = os.path.join(scripts, name)
        util.make_dir(root, d)
        p = os.path.join(root, d, "example_{}.py".format(filename))
        util.write(p, txt, overwrite)

    for d, ps in (
        ("canvas2D", ("canvas.yaml", "canvas_config.xml", "alt_config.xml")),
        ("extractionline", ("valves.yaml",)),
        ("monitors", ("system_monitor.cfg",)),
        ("", ("startup_tests.yaml", "experiment_defaults.yaml")),
    ):
        if d:
            out = os.path.join(sf, d)
            util.make_dir(sf, d)
        else:
            out = sf

        for template in ps:
            txt = render.render_template(template)
            p = os.path.join(out, template)
            util.write(p, txt, overwrite, verbose)

    ctx = {
        "canvas_path": os.path.join(sf, "canvas2D", "canvas.yaml"),
        "canvas_config_path": os.path.join(sf, "canvas2D", "canvas_config.xml"),
        "valves_path": os.path.join(sf, "extractionline", "valves.yaml"),
    }
    d = os.path.join(root, "preferences")
    util.make_dir(root, "preferences")
    p = os.path.join(d, "extractionline.ini")
    util.write(p, render.render_template("extractionline.ini", **ctx), overwrite)


def _code(fork, branch, app_id):
    update_root = os.path.join(HOME, f".pychron.{app_id}")
    ppath = os.path.join(update_root, "pychron")

    if not os.path.isdir(update_root):
        os.mkdir(update_root)

    if os.path.isdir(ppath):
        if not util.yes(
            "Pychron source code already exists. Remove and re-clone [y]/n"
        ):
            subprocess.call([GIT, "status"], cwd=ppath)
            return

        shutil.rmtree(ppath)

    url = f"https://github.com/{fork}/pychron.git"

    subprocess.call([GIT, "clone", url, f"--branch={branch}", ppath])
    subprocess.call([GIT, "status"], cwd=ppath)


def _launcher(
    conda, environment, app, org, app_id, login, msv, output, overwrite, verbose
):
    click.echo("launcher")
    template = "failed to make tmplate"
    if IS_MAC:
        if conda:
            template = "launcher_mac_conda"
        else:
            template = "launcher_mac"

    ctx = {
        "github_org": org,
        "app_name": app,
        "app_id": app_id,
        "use_login": login,
        "massspec_db_version": msv,
        "edm_envs_root": EDM_ENVS_ROOT,
        "edm_env": environment,
        "pychron_path": os.path.join(HOME, f".pychron.{app_id}", "pychron"),
    }

    txt = render.render_template(template, **ctx)

    if output is None:
        output = "pychron_launcher.sh"

    if verbose:
        click.echo(f"Writing launcher script: {output}")
        click.echo(txt)
    util.write(output, txt, overwrite)

    # make launcher executable
    subprocess.call(["chmod", "+x", output])


def _init(env, org, overwrite, verbose):
    click.echo("make initialization file")
    template = "initialization.xml"
    txt = render.render_template(template)
    if verbose:
        click.echo("======== Initialization.xml contents start ========")
        click.echo(txt)
        click.echo("======== Initialization.xml contents end ========")

    root = os.path.join(HOME, env)
    sf = "setupfiles"
    util.make_dir(root, sf)

    p = os.path.join(root, sf, "initialization.xml")
    util.write(p, txt, overwrite=overwrite)

    d = os.path.join(root, "preferences")
    util.make_dir(root, "preferences")

    template = "general.ini"
    txt = render.render_template(
        template, general_organization=org, general_remote="{}/Laboratory"
    )
    p = os.path.join(d, "general.ini")
    util.write(p, txt, overwrite=overwrite)

    template = "update.ini"
    txt = render.render_template(
        template,
        build_repo=os.path.join(HOME, ".pychron.0", "pychron"),
        build_remote="PychronLabsLLC/pychron",
        build_branch="dev/dr",
    )
    p = os.path.join(d, "update.ini")
    util.write(p, txt, overwrite=overwrite)

    template = "arar_constants.ini"
    txt = render.render_template(template)
    p = os.path.join(d, "arar_constants.ini")
    util.write(p, txt, overwrite=overwrite)


# ============= EOF =============================================
