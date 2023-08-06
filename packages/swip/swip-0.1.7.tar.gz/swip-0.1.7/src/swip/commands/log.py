from typing import Dict, List, Optional, Tuple

import networkx as nx
from matplotlib import pyplot as plt

from swip.common.paths import PATHS as path_to
import swip.common.helpers as helpers
from swip.common.exceptions import CommitRequiredError
from swip.common.helpers import logger, HEAD


def get_branch_history(head_commit: str, history: List) -> Optional[Dict[str, str]]:
    """Returns a list of dictionaries containing the history 
    of a given branch. Each record contains a commit id, the 
    date and time, the commit message and the commit's parent(s).
    """
    if head_commit == 'None':
        return

    for res in history:
        if res['commit'] == head_commit:
            return

    commit_file = path_to.images.joinpath(head_commit + '.txt')    
    with open(commit_file, 'r') as commit_txt:
        lines = commit_txt.readlines()

    res = {}
    res['commit'] = head_commit
    _, parents = lines[0].strip().split("=")  
    res['date'] = lines[1].strip().split("=")[1]
    res['message'] = lines[2].strip().split("=")[1]
    
    if ',' not in parents:
        res['parents'] = [parents]
        history.append(res)
        return get_branch_history(parents, history)

    parent1, parent2 = parents.split(',')
    res['parents'] = [parent1, parent2]
    history.append(res)
    get_branch_history(parent2.strip(), history)
    return get_branch_history(parent1.strip(), history)


def get_log_history(
    all: bool, commits: List[str], head_commit: str
    ) -> List[Dict[str, str]]:
    """Given all is True, returns a history information
    of all existing branches . Otherwise, returns only
    the history of the current active branch. 
    """
    history = []
    if all:
        for commit in commits:
            get_branch_history(commit, history)
    else:
        get_branch_history(head_commit, history)
    return history


def add_branches_pointers_to_log(
    log: List[Dict[str, str]], branches_info: Dict[str, str]
    ) -> None:
    """Given branch history list returned by get_branch_history,
    and a dictionary containing branches and their respective
    commit ids, adds to the commit's value in the branch history
    the pointed branch's name and HEAD.
    """
    active_branch = helpers.get_active_branch()
    for branch, commit in branches_info.items():
        if active_branch == branch:
            branch = f'{HEAD} -> {branch}'
        for dict in log:
            if dict['commit'] == commit:
                dict['commit'] += f' ({branch})'
 

def print_log(log: List[Dict[str, str]]) -> str:
    """Iterate over the log list of dictionaries, where each 
    dictionary represents a commit id info, to build a string
    containing all the commits information.
    """
    info = ""
    for image in log:
        info += f"Commit: {image['commit']}\n"
        if len(image['parents']) > 1:
            parent1, parent2 = image['parents']
            info += f"Merged: {parent1[:6]} {parent2[:6]}\n"
        info += f"Date: {image['date']}\n"
        info += f"Message: {image['message']}\n\n"
    print(info)


def get_branch_pointers(head_commit, branches_commits):
    """Returns a list of tuples containing branches and 
    their respective HEAD pointers.
    """
    pointers = []
    pointers.append((HEAD, head_commit[:6]))
    for branch, commit in branches_commits.items():
        pointers.append((branch, commit[:6]))
    return pointers


def create_graph(log: List[Dict[str, str]], branch_pointers: Tuple[str, str]) -> None:
    """Iterates over the log dictionary and creates the graph
    which will be drawn to the user based on these links.
    """
    parents = {l['commit']: l['parents'] for l in log
            if l['parents'] != ['None']}
    parents_edges = [
        (node[:6], parent[:6])
        for node, parents in parents.items()
        for parent in parents]

    # dot = graphviz.Digraph(format='svg')
    # dot.edges(parents_edges)
    # dot.edges(branch_pointers)
    # dot.render(directory='.swip/doctest-output', view=True) 
    g = nx.DiGraph()
    g.add_edges_from(parents_edges)
    g.add_edges_from(branch_pointers)
    nx.draw_networkx(g, arrows=True)
    plt.show()


   

def log(graph=False, all=False):
    """Prints a branch history. If 'all' options is used,
    the history of all branches combined is printed.
    If 'graph' is used, a graph of the history is shown
    to the user.
    """
    try:
        helpers.validate_ref_file_exists()
    except CommitRequiredError as err:
        logger.warning(err)
        return False

    head_commit = helpers.get_head_commit_id()
    branches_and_commits = helpers.get_all_branches_commits()
    branches_last_commits = branches_and_commits.values()
    history = get_log_history(all, branches_last_commits, head_commit)
    
    add_branches_pointers_to_log(history, branches_and_commits)
    print_log(history)

    if graph:
        graph_pointers = get_branch_pointers(head_commit, branches_and_commits)
        create_graph(history, graph_pointers) 
    return True
    