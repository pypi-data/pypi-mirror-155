import random
import shutil
import string
from datetime import datetime

import swip.common.helpers as helpers
from swip.common.exceptions import CommitError
from swip.common.paths import PATHS as path_to
from swip.common.helpers import logger, HEAD

from swip.commands.status import get_status_info


def is_commit_allowed() -> None:  # Convention: returns True or False 
    """Checks the staging area directory. Throws CommitError
    if the staging directory is empty, or if no changes were
    made since last commit, causing the commit command to
    fail.
    """ 
    staging_content = list(path_to.staging_area.iterdir())
    if not staging_content:
        raise CommitError("Use the add command in order to add files to commit")    
    
    if path_to.references.exists():
        status = get_status_info()
        if not status.to_commit:  
            raise CommitError('No Files added to commit')
            

def generate_commit_id(commit_len: int = 40) -> str:
    """Returns a string consisting of 40 chars randomly
    selected from 0-9 & a-z.
    """
    chars = string.ascii_lowercase + string.digits
    commit_id = "".join(random.choice(chars) for _ in range(commit_len))
    return commit_id


def create_commit_dir(commit_id: str) -> str: 
    """Creates a new image commit directory within the images
    directory, which will contain the current staging area
    content.
    """
    commit_path = path_to.images / commit_id
    commit_path.mkdir()
    return commit_path
    

def create_image(commit_path: str) -> None:
    """Copies the content of the staging area to 
    a given commit directory path. Dirs that exists will not
    be replaced, files that exist will be overwritten.
    """
    destination = commit_path
    shutil.copytree(path_to.staging_area, destination, dirs_exist_ok=True)
    

def create_commit_metadata(commit_path: str, message: str, parents) -> None: 
    """Creates a commit metadata text file inside the images dir, 
    and writes the following information for each commit: 
    The commit's parent(s) if exists, the current time and date,
    and the commit message entered by the user. The file name
    is identical to the commit's directory name.
    """
    current_time = str(datetime.now().strftime("%a %b %w %H:%M:%S %Y"))
    if not parents:
        parents = helpers.get_head_commit_id() if path_to.references.exists() else None
    with open(f"{commit_path}.txt", "w") as file:
        to_write = [f"parent={parents}\n", f"date={current_time}\n", f"message={message}\n\n"] 
        file.writelines(to_write)


def update_references_file(commit_id):
    """Updates the HEAD & branch pointers in the references 
    file to the new commit id. If HEAD and the branch point 
    to the same commit, the branch's commit id will 
    be updated as well.
    """
    active = helpers.get_active_branch()
    head = helpers.get_head_commit_id()
    with open(path_to.references, "r") as file: 
        ref_lines = file.readlines()
    
    new_txt = ''
    for line in ref_lines:
        if line.startswith(HEAD): 
            line = line.replace(head, commit_id)
        branch_name, branch_commit = line.strip().split('=')
        if branch_commit == head and branch_name == active:
            line = line.replace(branch_commit, commit_id)
        new_txt += line
    return new_txt


def handle_references(commit_id: str) -> None:
    """Handles the update or creation of the references file.
    If it's the first commit, i.e. file does not exist,
    references file will be created. Otherwise, it will be
    updated.
    """
    if not path_to.references.exists(): 
        helpers.create_references_file(commit_id)
        return
    new_refs_txt = update_references_file(commit_id) 
    with open(path_to.references, "w") as file:
        file.write(new_refs_txt)
         

def commit(message: str, parents=None) -> bool:
    """Commits changes that were added to the staging area."""
    try:
        is_commit_allowed() 
    except CommitError as err:
        logger.warning(err)
        return False
    commit_id = generate_commit_id() 
    commit_path = create_commit_dir(commit_id)
    create_commit_metadata(commit_path, message, parents)
    create_image(commit_path) 
    handle_references(commit_id)
    logger.info(f'Commit {commit_id[:6]} created')
    return True 

