import os as _os
import subprocess as _subprocess

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
def init():
    rich.print("initializing python project agilely...")
    _dir = _os.path.dirname(_os.path.abspath(__file__))
    settings_dir = _os.path.join(_dir, "..", "settings")

    rich.print("generating ./vscode/settings.json...")
    vscode_path = _os.path.join(settings_dir, "vscode_settings.json")
    target_path = _os.path.join(".vscode", "settings.json")
    actions.copy_serializable(
        vscode_path, target_path, transform=actions.vscode_setting_transform, conflict="merge"
    )

    rich.print("generating ./.pre-commit-config.yaml...")
    precommit_path = _os.path.join(settings_dir, "pre-commit-config.yaml")
    actions.copy_serializable(precommit_path, ".pre-commit-config.yaml", conflict="merge")

    rich.print("generating ./pyproject.toml...")
    pyproject_path = _os.path.join(settings_dir, "pyproject.toml")
    actions.copy_serializable(
        pyproject_path, "pyproject.toml", transform=actions.pyproject_transform, conflict="merge"
    )

    rich.print("generating ./.gitignore.toml...")
    gitignore_path = _os.path.join(settings_dir, "gitignore")
    actions.copy_serializable(gitignore_path, ".gitignore", conflict="merge")

    rich.print("creating git information...")
    actions.git_init()

    rich.print("setting pre-commit hook...")
    hook_script = _os.path.join(_dir, "..", "scripts", "precommit_hook.sh")
    _subprocess.run(["bash", hook_script])
