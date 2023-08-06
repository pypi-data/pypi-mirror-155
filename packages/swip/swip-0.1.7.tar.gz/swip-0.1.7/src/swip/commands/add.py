import shutil
from pathlib import Path

import swip.common.helpers as helpers
from swip.common.paths import PATHS as path_to
from swip.common.helpers import logger


def validate_path(input_path):
    """Checks if the user input path matches an existing
    file. Returns the absolue path on success, otherwise
    FileNotFoundError is thrown.
    """
    abs_path = input_path.resolve()
    if not abs_path.exists(): 
        raise FileNotFoundError(
            f"{abs_path} does not match an existing file"
            )
    return abs_path


def copy_subdir_to_staging(working_dir: Path, dir: Path) -> None:
    """Given a path to a directory, it will be
    copied recursively to the staging area of the swip 
    repository. Parent directories are created if missing.
    """
    relative_path = dir.relative_to(working_dir)
    destination = path_to.staging_area / relative_path
    shutil.copytree(dir, destination, dirs_exist_ok=True)


# This is working, but repeats itself.
def copy_working_directory(working_dir: Path) -> None:
    """Given the input path is the working directory itself,
    the working dir contents will be copied, excluding
    the .swip repo and its content.
    """
    paths_to_copy = helpers.get_rel_paths(working_dir, exclude_swip=True)
    for path in paths_to_copy:
        if path.is_file():
            helpers.copy_file_to_staging(working_dir, path)
        if path.is_dir():
            path = working_dir / path
            copy_subdir_to_staging(working_dir, path)


def handle_copying_to_staging(path: Path) -> None:
    """Given a path, checks if the path is the working
    directory itself, a subdirectory, or a file. 
    For each option, the appropriate copying function 
    will be excecuted.
    """
    working_dir = path_to.working_dir
    if path == working_dir:
        copy_working_directory(working_dir)
        return
    if path.is_file():
        file_rel_path = path.relative_to(working_dir)
        helpers.copy_file_to_staging(working_dir, file_rel_path)
        return 
    copy_subdir_to_staging(working_dir, path)


def add(path: str) -> bool:
    """Adds a file or directory path to the staging area."""
    user_path = Path(path)
    try:
        abs_path = validate_path(user_path)
    except FileNotFoundError as er:
        logger.warning(er)
        return False
    handle_copying_to_staging(abs_path)
    return True