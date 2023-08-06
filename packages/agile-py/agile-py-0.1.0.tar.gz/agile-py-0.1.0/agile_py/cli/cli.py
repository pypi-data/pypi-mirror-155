from __future__ import annotations

import os as _os
import subprocess as _subprocess
from typing import Union

import click as _click
import rich

from . import actions


class RunGroup(_click.Group):
    def get_command(self, ctx, cmd_name):
        rv = _click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        return None


@_click.command(cls=RunGroup, invoke_without_command=True)
@_click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        _click.echo(ctx.get_help())


@cli.command("init", help="init python project")
@_click.option(
    "-rm",
    "--readme",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable adding new template `README.md` file.",
)
@_click.option(
    "-vs",
    "--vscode_setting",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable adding and merging vscode setting file.",
)
@_click.option(
    "-pc",
    "--precommit",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable adding and merging precommit file.",
)
@_click.option(
    "-l",
    "--license",
    default=None,
    help="License of the project, can be [Apache2, BSD3, GPL3, LGPL, MIT].",
)
@_click.option(
    "-p",
    "--package",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable adding template `setup.py` file.",
)
@_click.option(
    "-ga",
    "--github_action",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable adding github_action file for pypi.",
)
@_click.option(
    "-a",
    "--all_bool",
    default=False,
    is_flag=True,
    show_default=True,
    help="Enable adding all bool FLAGS.",
)
def init(
    readme: bool,
    vscode_setting: bool,
    precommit: bool,
    license: Union[str, None],
    package: bool,
    github_action: bool,
    all_bool: bool,
):
    rich.print("initializing python project agilely...")
    _dir = _os.path.dirname(_os.path.abspath(__file__))
    settings_dir = _os.path.join(_dir, "..", "settings")

    rich.print("generating ./.gitignore.toml...")
    gitignore_path = _os.path.join(settings_dir, "gitignore")
    actions.copy_serializable(gitignore_path, ".gitignore", conflict="merge")

    rich.print("creating git information...")
    actions.git_init()

    if readme or all_bool:
        rich.print("generating README.md...")
        read_pathme = _os.path.join(settings_dir, "README.md")
        actions.overwrite_serializable(read_pathme, "README.md", ask=True)

    if vscode_setting or all_bool:
        rich.print("generating ./vscode/settings.json...")
        vscode_path = _os.path.join(settings_dir, "vscode_settings.json")
        target_path = _os.path.join(".vscode", "settings.json")
        actions.copy_serializable(
            vscode_path, target_path, transform=actions.vscode_setting_transform, conflict="merge"
        )

    if precommit or all_bool:
        rich.print("generating ./.pre-commit-config.yaml...")
        precommit_path = _os.path.join(settings_dir, "pre-commit-config.yaml")
        actions.copy_serializable(precommit_path, ".pre-commit-config.yaml", conflict="merge")

        rich.print("generating ./pyproject.toml...")
        pyproject_path = _os.path.join(settings_dir, "pyproject.toml")
        actions.copy_serializable(
            pyproject_path,
            "pyproject.toml",
            transform=actions.pyproject_transform,
            conflict="merge",
        )

        rich.print("setting pre-commit hook...")
        hook_script = _os.path.join(_dir, "..", "scripts", "precommit_hook.sh")
        _subprocess.run(["bash", hook_script])

    if license is not None:
        license_path = actions.select_license(license)
        license_path = _os.path.join(settings_dir, license_path)
        actions.overwrite_serializable(license_path, "LICENSE", ask=True)

    if package or all_bool:
        setup_path = _os.path.join(settings_dir, "setup.py")
        actions.overwrite_serializable(setup_path, "setup.py", ask=True)

    if github_action or all_bool:
        ga_path = _os.path.join(settings_dir, "ga", "publish-to-pypi.yml")
        target_path = _os.path.join(".github", "workflows", "publish-to-pypi.yml")
        actions.overwrite_serializable(ga_path, target_path, ask=True)
