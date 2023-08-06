from pathlib import Path

from swip.common.helpers import logger


def create_swip_subdirs(repo_path: Path) -> None: 
    """Creates the images and staging_area subdirs in 
    the swip rpository.
    """
    for subdir in ['images', 'staging_area']:
        joined_path = repo_path / subdir
        joined_path.mkdir()


def create_activated_file(repo_path: str) -> None:
    """Creates a text file named activated, which will 
    contain the currnet active branch name.
    """
    activated_file = repo_path / 'activated.txt'
    with open(activated_file, 'w') as file:
        file.write('master')


def init(): 
    """Initializes a swip repository in project directory."""
    cwd = Path.cwd()
    swip_repo = cwd.joinpath('.swip')
    
    try:
        swip_repo.mkdir()
    except OSError:
        logger.warning(f'A Swip repository already initiated in {cwd}') 
        return False

    create_swip_subdirs(swip_repo) 
    create_activated_file(swip_repo)
    logger.info(f'Initialized in {swip_repo}. Ready to go!')
    return True
