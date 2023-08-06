import filecmp
from pathlib import Path
from typing import NamedTuple, Optional, Set

import swip.common.helpers as helpers
from swip.common.exceptions import CommitRequiredError
from swip.common.paths import PATHS as path_to
from swip.common.helpers import logger


class Status(NamedTuple):
    active_branch: str
    to_commit: str
    not_staged: str
    untracked_files: str


# currenly no support for dirs.
# To do? this function is too similar to compare dirs in Merge.
def get_to_be_committed(last_commit_id: str) -> Set[Optional[Path]]:
    """Iterates over staging area dir in search for files that 
    are in the staging area but not in the last commit. For files 
    that are in both, a comparison will be executed to check if
    changes were made. Returns a set containing newly added and 
    changed files & dirs. 
    """ 
    commit_dir = path_to.images / last_commit_id 
    staging_paths = helpers.get_rel_paths(path_to.staging_area, only_files=True) 
    diff = set()
    for path in staging_paths:
        file_in_staging = path_to.staging_area / path
        file_in_commit = commit_dir / path
        if not file_in_commit.exists():
            diff.add(path)
        elif not filecmp.cmp(file_in_staging, file_in_commit, shallow=False):
            diff.add(path)
    return diff
        

def get_not_staged() -> Set[Optional[Path]]:
    """Finds and compares the mutual files of staging area
    and working directory. Returns a set containing the files
    in which changes were made since last commit.
    """
    diff = set()
    staging_files = helpers.get_rel_paths(path_to.staging_area, only_files=True)
    working_dir_files = helpers.get_rel_paths(path_to.working_dir, only_files=True) 
    mutual_files = staging_files & working_dir_files
    diff = helpers.get_diff_content_files(mutual_files, path_to.staging_area, path_to.working_dir)
    return diff


def get_untracked_files() -> Set[Optional[Path]]:
    """Compares the content of the working directory - excluding the swit
    repository content - and the content of the staging area. Returns a 
    set containing the files that are in the working directory but
    not in the staging area.
    """
    diff = set()
    working_dir_paths = helpers.get_rel_paths(path_to.working_dir, exclude_swip=True)
    staging_paths = helpers.get_rel_paths(path_to.staging_area)
    diff = working_dir_paths - staging_paths
    return diff


def get_status_info() -> NamedTuple: 
    """Returns a NamedTuple containing the current commit id and 
    all the status sections - changes to be committed, changed not
    staged for commit and untracked files.
    """
    try:
        cur_commit = helpers.get_head_commit_id()
    except FileNotFoundError:
        raise CommitRequiredError("Can't be executed before first commit")

    active_branch = helpers.get_active_branch()
    to_commit = get_to_be_committed(cur_commit)
    not_staged = get_not_staged()
    untracked_files = get_untracked_files()
    cur_status = Status(
        active_branch, to_commit, not_staged, untracked_files
    )
    return cur_status

 
def prettify_section(section: Set[Optional[str]]) -> str:
    """Given a set of paths, returns a string of these paths."""
    to_print = ''
    if not section:
        return ' -\n' 
    for path in section:
        to_print += f' {path}\n'
    return to_print
    

def print_status(status: NamedTuple) -> None:
    """Given current status info and current active branch, 
    prints all info to the user.
    """
    print('-' * 15)
    print(f'On branch: {status.active_branch}')
    print(f'Changes to be committed:\n{prettify_section(status.to_commit)}')
    print(f'Changes not staged:\n{prettify_section(status.not_staged)}')
    print(f'Untracked files:\n{prettify_section(status.untracked_files)}')
 

def status():
    try:
        cur_status = get_status_info()
    except CommitRequiredError as err:
        logger.warning(err)
        return False
        
    print_status(cur_status)
    return True

    


