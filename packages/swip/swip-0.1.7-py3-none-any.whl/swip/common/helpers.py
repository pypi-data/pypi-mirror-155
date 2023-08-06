import filecmp
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

from loguru import logger

from swip.common.exceptions import CommitRequiredError
from swip.common.paths import PATHS as path_to


HEAD = 'HEAD'


def is_working_tree_clean(cur_status):
    """Returns False if there are changes to be commited 
    or changes not staged for commit. Returns True otherwise.
    """
    return not cur_status.to_commit and not cur_status.not_staged


# Commits 
def get_head_commit_id() -> str:
    """Return the commit id HEAD points to."""
    with open(path_to.references, 'r') as file:
        head_line = file.readline() 
    _, commit_id = head_line.split('=') 
    return commit_id.strip()   


def get_commit_by_branch(input_branch: str) -> Optional[str]: 
    """Given a branch name, returns it's latest
    commit id from the references file if branch
    exists. Otherwise, returns None.
    """
    with open(path_to.references, "r") as file:
        ref_txt = file.readlines()
    for line in ref_txt: 
        branch_name, commit_id = line.strip().split('=')
        if input_branch == branch_name:
            return commit_id
    return 


def get_all_branches_commits() -> Dict[str, str]:
    """Reads references and returns a dictionary containing
    key: value pairs of branch name: last commit id.
    """
    branches_commits = {}
    with open(path_to.references, 'r') as ref_file:
        ref_text = ref_file.readlines()
    for line in ref_text[1:]:
        branch, commit = line.strip().split('=')
        branches_commits[branch] = commit
    return branches_commits


# Refernces file
def create_references_file(commit_id: str) -> None:
    """Creates the references text file in the swip repository, which 
    will contain all existing branches and the current commit
    they point to, as well as the HEAD current commit. Each line 
    represents a specific branch in the format <branch name>=<commit id>.
    """
    with open(path_to.references, "w") as file:
        to_write = [f"HEAD={commit_id}\n", f"master={commit_id}"]
        file.writelines(to_write)


def validate_ref_file_exists():
    """Checks if references file exists. If not, 
    CommitRequiredError is raised."""
    if not path_to.references.exists():
        raise CommitRequiredError(
            "Can't be executed before first commit"
        )


def update_ref_head(commit_id: str) -> None: 
    with open(path_to.references, "r") as file:
        ref_txt = file.readlines()
        _, current_commit_id = ref_txt[0].strip().split('=')
        ref_txt[0] = ref_txt[0].replace(current_commit_id, commit_id)
    
    with open(path_to.references, "w") as file:
        file.writelines(ref_txt)
        

# Branches
def get_active_branch() -> str:
    """Reads activated file and returns current
    activated branch.
    """
    active_branch = path_to.activated.read_text()
    return active_branch


def get_existing_branches() -> List[str]:
    """Return a list of all existing branches."""
    branches_info = get_all_branches_commits()
    branches_names = branches_info.keys()
    return branches_names


# Files
def get_rel_paths(
    dir: Path, only_files: bool = False, exclude_swip: bool = False
    ) -> Set[Path]:
    """Given a path to a directory, returns all its content paths, 
    relative to the given directory.

    If only_files is True, only files paths are returned. exclude_swip
    is used on the working directory. If True, returns all working 
    directory files excluding the swip repository content.
    """
    paths = set(dir.rglob('*'))
    if exclude_swip and only_files:
        return {p.relative_to(dir) for p in paths if 
        not p.is_relative_to(path_to.swip) and p.is_file()}
    
    if exclude_swip:
        return {p.relative_to(dir) for p in paths if 
        not p.is_relative_to(path_to.swip)}

    if only_files:
        return {p.relative_to(dir) for p in paths if p.is_file()}

    return {p.relative_to(dir) for p in paths}


def get_diff_content_files(
    mutual_files: Set[Path], dir_one_path: Path, dir_two_path: Path
    ) -> Set[Path]:
    """Given a set of mutual files which appear in both directories, 
    joins the relative path of each file to each directory path and
    compares its content. Return a set of files with different content.
    """
    changed_files = set()
    for file_path in mutual_files:
        file_one = dir_one_path / file_path
        file_two = dir_two_path / file_path
        if not filecmp.cmp(file_one, file_two, shallow=False):
            changed_files.add(file_path)
    return changed_files
    

def copy_file_to_staging(source_dir: Path, file: Path) -> None: 
    """Given a file's path, file will be copied
    to the staging area of the swip repository.
    """
    destination = path_to.staging_area / file
    destination_dir = destination.parent
    if not destination_dir.exists():
        destination_dir.mkdir(parents=True)
    abs_path = source_dir / file
    shutil.copy(abs_path, destination)


def update_working_dir(
    source_dir: Path, paths_to_keep: Optional[Set[str]] = None
    ) -> None: 
    """Given a source directory - such as staging area or
    a commit image -  updates the working dir to match the
    content of the source dir without altering or deleting
    the swip repsitory.
    
    If paths_to_keep is given, these files and dirs paths will
    also be ignored in the updating process.
    """

    working_dir_paths = get_rel_paths(path_to.working_dir, exclude_swip=True)
    if paths_to_keep:
        working_dir_paths = working_dir_paths - paths_to_keep
    for path in working_dir_paths:
        path = path_to.working_dir / path 
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=False)
        elif path.is_file():
            path.unlink()
    shutil.copytree(source_dir, path_to.working_dir, dirs_exist_ok=True)


# logger formatting 
logger.remove()
logger.add(sys.stdout, format='{time:%H:%M:%S} | {module}: <lvl><n>{message}</></>')
