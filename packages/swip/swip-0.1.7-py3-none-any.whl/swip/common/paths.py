from pathlib import Path

from swip.common.exceptions import NoSwipError


def find_swip_repo(given_path):  
    path = Path(given_path)
    swip_path = None
    if path.is_file():
        path = path.parent

    while path != path.parent and swip_path is None:
        subdirs = [p for p in path.iterdir() if p.is_dir()] 
        for dir in subdirs:
            if dir.name == ".swip":
                swip_path = dir
                return swip_path
        path = path.parent
    raise NoSwipError(
        'No .Swip repository in this directory or any of its parents'
        )


class SwipPaths:
    swip: Path
    working_dir: Path
    images: Path
    staging_area: Path
    references: Path
    activated: Path


PATHS = SwipPaths()

def create_swip_paths(swip):
    PATHS.swip = swip
    PATHS.working_dir = swip.parent
    PATHS.images = swip / 'images'
    PATHS.staging_area = swip / 'staging_area'
    PATHS.references = swip / 'references.txt'
    PATHS.activated = swip / 'activated.txt'
