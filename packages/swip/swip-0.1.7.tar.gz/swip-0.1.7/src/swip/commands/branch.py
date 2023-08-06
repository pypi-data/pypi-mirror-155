from typing import Optional

import swip.common.helpers as helpers
from swip.common.exceptions import BranchExistsError, CommitRequiredError
from swip.common.paths import PATHS as path_to
from swip.common.helpers import logger
from termcolor import colored


def validate_new_branch_name(name: str) -> None:  
    """Given a branch name, reads and iterates over
    the references file. If a matching existing branch 
    name is found, BranchExistsError will be raised
    and the branch command will fail.
    """
    with open(path_to.references, 'r') as file:
        ref_text = file.readlines()
    for line in ref_text:
        branch_name, _ = line.split('=')
        if name == branch_name:
            raise BranchExistsError(f'Branch {name} already exists')


def print_existing_branches() -> None:
    """Prints all existing branch names."""
    branches = helpers.get_existing_branches()
    active = helpers.get_active_branch()
    avail_branches = ''
    for branch in branches:
        if branch == active:
            branch = colored(f'*{branch}', 'cyan')
        avail_branches += f'{branch}\n'
    print(avail_branches)


def add_branch_to_ref(name: str, commit_id: str) -> None:
    """Adds branch name to references file with
    a pointer to the current (HEAD) commit id.
    """
    with open(path_to.references, "a") as file:
        file.write(f"\n{name}={commit_id}")


def branch(name: Optional[str] = None) -> bool:
    """If name was given, a branch with that name is created.
    Otherwise, all branches will be printed.
    """ 
    try:
        helpers.validate_ref_file_exists()
    except CommitRequiredError as err:
        logger.warning(err)
        return False

    if not name:
        print_existing_branches()
        return True

    try:
        validate_new_branch_name(name)
    except BranchExistsError as err:
        logger.warning(err)
        return False

    cur_commit_id = helpers.get_head_commit_id() 
    add_branch_to_ref(name, cur_commit_id) 
    logger.info(f'Branch {name} created')
    return True
