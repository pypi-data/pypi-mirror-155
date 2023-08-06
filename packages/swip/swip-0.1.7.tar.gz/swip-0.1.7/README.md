# swip 
A Python implementation of the version control system, Git. 
Motivated to gain a deep understanding of Git, the project implements 
Git’s basic functionality.

## How to install?
install via pip
```
 pip install swip
```

## How to use swip?
* `swip init` initiates a new swip repository.
* `swip add` adds file/s or directory to the next commit.
* `swip commit` creates a snapshot of the reposistory.
   each commit requires a message.
* `swip branch` shows the current active branch.
    To create a new branch use `swip branch -m <branch name>`.
* `swip checkout <name>` switches to a given branch or commit id
    and updates the repository and the working directory.
* `swip status` shows which changes have been staged, which changes haven't
    and files which currenly are not tracked by swip.
* `swip log` shows the current barnch commit history starting from HEAD.  
    To get all branches history, use `-all`.  
    To get a graph visualization use `-graph`.
* `swip merge` incorporates changes from a given branch into the current active branch.  
    Currently this is a basic implementation of git merge meaning merge conflicts  
    are handled by commiting the last changed files.
