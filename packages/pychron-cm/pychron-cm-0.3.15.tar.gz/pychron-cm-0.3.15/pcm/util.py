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


def yes(msg):
    if not msg.endswith(" "):
        msg = "{} ".format(msg)

    return input(msg) in ("", "y", "yes", "Yes", "YES")


def make_dir(root, name):
    for d in (root, os.path.join(root, name)):
        if not os.path.isdir(d):
            os.mkdir(d)


def write(p, t, overwrite=False, verbose=False):
    if not os.path.isfile(p) or overwrite:
        click.echo(f"wrote file: {p}")
        if verbose:
            click.secho(f"{p} contents: ==============", fg="blue")
            click.secho(t, fg="yellow", bg="black")
            click.secho(f"{p} end: ================================", fg="blue")
        with open(p, "w") as wfile:
            wfile.write(t)
    else:
        click.secho(f"file already exists skipping: {p}", fg="red")


def echo_config(*args):
    click.secho("------------ Configuration -------------", fg="yellow")
    for a in args:
        click.secho(f"={a}", fg="yellow")
    click.secho("------------ Configuration End -------------", fg="yellow")


# ============= EOF =============================================
