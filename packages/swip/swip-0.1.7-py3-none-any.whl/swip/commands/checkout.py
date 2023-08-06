import shutil
from collections import namedtuple
from pathlib import Path
from typing import Optional, Set, Tuple

import swip.common.helpers as helpers
from swip.common.exceptions import CheckoutError, CommitRequiredError
from swip.common.paths import PATHS as path_to
from swip.common.helpers import logger

from swip.commands.status import get_status_info, print_status


def is_valid_branch(destination: str) -> Optional[str]:
    """Given the user input, checks if it matches a 
    branch name. If so, returns the commit id of the
    branch. Otherwise, returns None.
    """
    commit_id = helpers.get_commit_by_branch(destination)
    return None if not commit_id else commit_id

    
def verify_commit_id(commit_id: str) -> bool:
    """Returns True if commit_id matches an existing
    commit. Otherwise, returns False.
    """
    commit_dir_path = path_to.images / commit_id
    return commit_dir_path.exists()


def validate_checkout(status: namedtuple, destination: str) -> Tuple[str, str]:
    """Checkout command will fail if one of these
    conditions are met:
    - There are changes to be commited or changes not staged.
    - User destination input doesn't match a branch name or 
    a commit id known to Swip.

    If a branch name was given, returns a tuple of branch name
    and its HEAD commit id. If branch wasn't given, branch 
    name will be None. On failure, CheckoutError will be thrown.
    """
    branch = None
    if not helpers.is_working_tree_clean(status):
        print_status(status)
        raise CheckoutError(
            'In order to Checkout, pleae clear your working tree'
        )
    
    commit_by_branch = is_valid_branch(destination)
    if commit_by_branch:
        branch = destination
        commit_id = commit_by_branch
        return branch, commit_id

    if not verify_commit_id(destination):
        raise CheckoutError("Input doesn't match any commit or branch")
    
    commit_id = destination
    return branch, commit_id


def update_staging_area(commit_dir: Path) -> None:
    """Removes all staging area content and replaces it
    with the given commit directory content.
    """
    shutil.rmtree(path_to.staging_area, ignore_errors=False)
    shutil.copytree(commit_dir, path_to.staging_area, dirs_exist_ok=True)


def paths_to_ignore(untracked_files: Set[Optional[Path]]) -> Set[Optional[Path]]: 
    """Given a Set of untracked files, returns the
    files' paths, including parent directories, to ignore. 
    """
    working_dir = path_to.working_dir
    paths_to_ignore = set()
    for path in untracked_files:
        path = working_dir / path
        while path != working_dir:
            paths_to_ignore.add(path.relative_to(working_dir)) 
            path = path.parent
    return paths_to_ignore  



def update_active_branch(branch_name: str) -> None:
    """Overwrites activated file to contain the given branch,
    which will become the active branch.
    """
    path_to.activated.write_text(branch_name)
            

def checkout(destination: str) -> bool:
    """Checks out a branch or a commit id.
    The given content of the commit id or HEAD of
    given branch will be copied to the working
    directory and the staging area.
    """
    try:
        status = get_status_info()
    except CommitRequiredError as err:
        logger.warning(err)
        return False

    try:
        branch, commit_id = validate_checkout(status, destination)
    except CheckoutError as err:
        logger.warning(err)
        return False

    commit_dir = path_to.images/ commit_id
    update_staging_area(commit_dir)
    untracked_paths = paths_to_ignore(status.untracked_files) 
    helpers.update_working_dir(commit_dir, paths_to_keep=untracked_paths)

    if branch:
        update_active_branch(branch)
    helpers.update_ref_head(commit_id)
    logger.info(f'Switched to {destination}') 
    return True   
    