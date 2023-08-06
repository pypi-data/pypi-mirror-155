from __future__ import annotations

import os as _os
import shutil as _shutil
import subprocess as _subprocess
from typing import Callable, Optional

import rich
from open_serializer import Serializer, merge_dict_recursively

from . import utils


def git_init() -> None:
    if utils.check_is_git():
        rich.print("git already exists, skipping...")
    else:
        _subprocess.run(["git", "init"])


def vscode_setting_transform(settings: dict) -> None:
    which_black = _subprocess.run(["which", "black"], stdout=_subprocess.PIPE)
    which_black = which_black.stdout.decode("utf-8").strip()
    settings["python.formatting.blackPath"] = which_black


def pyproject_transform(settings: dict) -> None:
    import sys

    py_version = sys.version_info
    py_version = f"py{py_version[0]}{py_version[1]}"
    if py_version not in settings["tool"]["black"]["target-version"]:
        settings["tool"]["black"]["target-version"].append(py_version)


def select_license(license: str) -> str:
    if license in ["apache", "apache2", "Apache", "Apache2", "Apache-2", "Apache-2.0"]:
        path = _os.path.join("license", "APACHE2")
    elif license in ["bsd", "bsd3", "BSD", "BSD3"]:
        path = _os.path.join("license", "BSD3")
    elif license in ["gpl", "gpl3", "GPL", "GPL3"]:
        path = _os.path.join("license", "GPL3")
    elif license in ["lgpl", "LGPL"]:
        path = _os.path.join("license", "LGPL")
    elif license in ["mit", "MIT"]:
        path = _os.path.join("license", "MIT")
    else:
        raise ValueError(f"invalid license: {license}")
    return path


def overwrite_serializable(ref_path: str, target_path: str, ask=False):
    if _os.path.exists(target_path):
        if ask:
            if utils.ask_bool(f"setting already exists at {target_path}, overwrite?"):
                _os.remove(target_path)
            else:
                return
    target_dir = _os.path.dirname(target_path)
    if target_dir and (not _os.path.isdir(target_dir)):
        _os.makedirs(target_dir)

    _shutil.copy2(ref_path, target_path)


def copy_serializable(
    ref_path: str,
    target_path: str,
    injections: Optional[dict] = None,
    transform: Optional[Callable] = None,
    conflict: str = "merge",
) -> None:
    settings = Serializer.deserialize_object(ref_path)
    if _os.path.exists(target_path):
        if conflict == "skip":
            rich.print(f"setting already exists at {target_path}, skipping...")
            return
        elif conflict == "merge":
            rich.print(f"setting already exists at {target_path}, merging...")
            merge_dict_recursively(
                settings,
                Serializer.deserialize_object(target_path),
                force_replace=True,
                skip_duplicated_list=True,
            )
        elif conflict == "ask_overwrite":
            is_y = utils.ask_bool(f"setting already exists at {target_path}, overwrite?")
            if is_y:
                _os.remove(target_path)
            else:
                return
        elif conflict == "overwrite":
            rich.print(f"setting already exists at {target_path}, overwriting...")
            _os.remove(target_path)
        else:
            raise ValueError(f"invalid conflict option: {conflict}")

    if injections is not None:
        settings.update(injections)

    if transform is not None:
        transform(settings)

    utils.require_folder(target_path)
    Serializer.serialize_object(settings, target_path)
