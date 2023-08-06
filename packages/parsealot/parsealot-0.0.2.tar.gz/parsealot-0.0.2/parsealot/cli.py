# Copyright (C) 2022 Leah Lackner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This is the main module docstring.

Some description comes here.
"""

import os
import os.path
import sys
from typing import Optional

import typer
from rich import print

# Allow running the main python script without installing the package
if __name__ == "__main__":
    import os as _os
    import sys as _sys

    _sys.path.append(_os.path.join(_os.path.dirname(__file__), ".."))

import parsealot.lib
from parsealot.__version__ import __version__

DEFAULT_COMMAND = "lib1"

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


def version_callback(value: bool) -> None:
    """
    Prints the version.
    """
    if value:
        print(
            f"[green]{os.path.basename(sys.argv[0])}:[/green]"
            f" [blue]v{__version__}[/blue]"
        )
        raise typer.Exit()


@app.command()
def lib1() -> None:
    """
    Calls an example library function.
    """
    parsealot.lib.some_lib_func()


@app.command()
def lib2() -> None:
    """
    Calls another library function.
    """
    parsealot.lib.other_lib_func()


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        False,
        "-v",
        "--version",
        help="Prints the version",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    Doctest test:

    >>> print("True")
    True
    """
    if ctx.invoked_subcommand is None:
        os.execv(sys.argv[0], [sys.argv[0], DEFAULT_COMMAND] + sys.argv[1:])


def main() -> None:
    """
    Runs the main application.
    """
    app()


if __name__ == "__main__":
    main()
