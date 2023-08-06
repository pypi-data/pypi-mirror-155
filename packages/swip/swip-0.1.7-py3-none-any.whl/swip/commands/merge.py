import shutil
from pathlib import Path
from typing import Set, Tuple

import swip.common.helpers as helpers
from swip.common.exceptions import CommitRequiredError, MergeError, NoBranchError
from swip.common.paths import PATHS as path_to
from swip.common.helpers import logger

import swip.commands.log as log
from swip.commands.commit import commit
from swip.commands.status import get_status_info, print_status


def validate_merge(branch_name):
    """Merge command will fail if one ot these
    conditions are met:
    - Given branch name doesn't match an existing branch,.
    - There are changes to be commited or changes not staged.
    """
    if branch_name not in helpers.get_all_branches_commits():
        raise NoBranchError('No such existing branch')

    status = get_status_info()
    if not helpers.is_working_tree_clean(status):
        print_status(status)
        raise MergeError('In order to Merge, please clear your working tree')
 
         
def find_mutual_ancestor(head_commit, branch_commit):
    """Given two commit ids, builds each commit's parents
    history and finds the first mutual commit of the two
    histories. 
    """
    active_history = []
    branch_history = []
    log.get_branch_history(head_commit, active_history)
    log.get_branch_history(branch_commit, branch_history)
    active_parents =  [commit['commit'] for commit in active_history]
    branch_parents = [commit['commit'] for commit in branch_history]
    for commit in branch_parents:
        if commit in active_parents:
            return commit
    return False
            

def compare_dir_files(
    branch_dir: Path, ancestor_dir: Path
    ) -> Tuple[Set[Path], Set[Path]]:
    """Returns files that were added to a branch and
    do not appear in the active branch, and the files
    that exist in both branches.
    """
    branch_files = helpers.get_rel_paths(branch_dir, only_files=True) 
    ancestor_files = helpers.get_rel_paths(ancestor_dir, only_files=True) 
    added_files = branch_files - ancestor_files
    mutual_files = branch_files & ancestor_files
    changed_files = helpers.get_diff_content_files(mutual_files, branch_dir, ancestor_dir) 
    return changed_files, added_files


def copy_changed_files(changed_files: Set[Path], branch_dir: Path) -> None:
    """Copies all changed files from the merged branch
    last commit to the staging area.
    """
    for file in changed_files:
        source_path = branch_dir / file
        dest_path = path_to.staging_area / file
        shutil.copy(source_path, dest_path)


def update_staging_area(
    branch_dir: Path, added_files: Set[Path], changed_files: Set[Path]
    ) -> None:
    """Copies all changed files and added files 
    (including missing parents) to staging area.
    """
    files_to_copy = added_files.union(changed_files) 
    for file in files_to_copy:
        helpers.copy_file_to_staging(branch_dir, file) 
    copy_changed_files(changed_files, branch_dir)


def merge_commit(branch_name: str, head_commit: str, branch_commit: str) -> None:
    """Executes a merge-commit: a commit
    that has two parents. The commit message
    indicates that it's a merge-commit.
    """
    active_branch = helpers.get_active_branch()
    merge_message = f'{branch_name} Merged into {active_branch} (HEAD)'
    parents = f'{head_commit},{branch_commit}'
    commit(merge_message, parents)


def merge(branch_name: str) -> bool:
    """Merges given branch name into current active branch."""
    try:
        validate_merge(branch_name)
    except (CommitRequiredError, MergeError, NoBranchError) as err:
        logger.warning(err)
        return False

    head_commit = helpers.get_head_commit_id() 
    branch_commit = helpers.get_commit_by_branch(branch_name)
    mutual_ancestor = find_mutual_ancestor(head_commit, branch_commit)
    branch_dir = path_to.images / branch_commit 
    ancestor_dir = path_to.images / mutual_ancestor
    changed_files, added_files = compare_dir_files(branch_dir, ancestor_dir)
    update_staging_area(branch_dir, added_files, changed_files)
    merge_commit(branch_name, head_commit, branch_commit)
    helpers.update_working_dir(path_to.staging_area) # what if there is untracked files?
    return True


