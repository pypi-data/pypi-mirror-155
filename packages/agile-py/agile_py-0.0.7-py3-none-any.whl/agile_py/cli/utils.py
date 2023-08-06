import os as _os
import subprocess as _subprocess


def check_is_git() -> bool:
    check = _subprocess.call(
        ["git", "branch"], stderr=_subprocess.STDOUT, stdout=open(_os.devnull, "w")
    )
    if check != 0:
        return False
    else:
        return True


def require_folder(path: str) -> None:
    dir = _os.path.split(path)[0]
    if dir:
        if not _os.path.isdir(dir):
            _os.makedirs(dir)
