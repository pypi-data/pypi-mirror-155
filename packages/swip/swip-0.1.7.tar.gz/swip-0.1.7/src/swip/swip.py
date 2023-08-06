import argparse
import os

from swip.commands.add import add
from swip.commands.branch import branch
from swip.commands.checkout import checkout
from swip.commands.commit import commit
from swip.commands.init import init
from swip.commands.log import log
from swip.commands.merge import merge 
from swip.commands.status import status
from swip.common.exceptions import NoSwipError
from swip.common.helpers import logger
from swip.common.paths import create_swip_paths, find_swip_repo



parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command', required=True)

# Init
init_parser = subparser.add_parser('init')

# Add
add_parser = subparser.add_parser('add')
add_parser.add_argument('path', type=str, help='a path to a file or a directory')

# Commit
commit_parser = subparser.add_parser('commit')
commit_parser.add_argument('message', type=str)

# Status
status_parser = subparser.add_parser('status')

# Branch
branch_parser = subparser.add_parser('branch')
branch_parser.add_argument('-name', '-n', metavar='<branch name>', type=str) 

# Checkout
checkout_parser = subparser.add_parser('checkout')
checkout_parser.add_argument('destination', metavar='[<branch name> | <commit id>]', type=str)

# Merge
merge_parser = subparser.add_parser('merge')
merge_parser.add_argument('branch_name', metavar='[<branch name>', type=str)

# Log
log_parser = subparser.add_parser('log')
log_parser.add_argument('-graph', action='store_true')
log_parser.add_argument('-all', action='store_true')


args = parser.parse_args()


COMMANDS = {
    'init': init,
    'add': add,
    'commit': commit,
    'status': status,
    'branch': branch,
    'checkout': checkout,
    'merge': merge,
    'log': log
}


def main():
    arg = args.command
    func = COMMANDS[arg]
    params = vars(args)
    command = params.pop("command")       
    
    if not command == 'init':
        cwd = os.getcwd()
        try:
            swip = find_swip_repo(cwd)
        except NoSwipError as err:
            logger.error(err)
            return

        create_swip_paths(swip)
    func(**params)


if __name__ == '__main__':
    main()
   