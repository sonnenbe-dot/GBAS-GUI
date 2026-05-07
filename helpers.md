

#Deploy on pip test server:
1) python -m build
2) py -m twine upload --repository testpypi dist/* --verbose (input API key)
3) pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade GBAS-package-sonnenbe-vers2

#Git commands:

a) Push changes to main branch
    1) git init (only when there is no hidden .git file in the location)
    2) git add . (add everything new)
    3) git commit -m "text-message"
    4) git push -u origin main (-u remembers which remote branch is tracked for future pushes, here it is tracked to origin, default name of the remote repo)
    5) git pull origin main (only if remote and local have both different changes, gain remote changes to local without overwriting local)

b) Change branch and push additions to new branch
    1) git switch <new branch name>
    2) git add . (add all new changes)
    3) git commit -m "text-message"
    4) git push -u origin <new branch name> (origin default name of remote branch)

c) Merging branch into main
    1) git switch main (switch to main branch)
    2) git pull origin main (get latest changes from remote main and merge it with local main branch without overwriting new local changes)
    3) git merge <branch_name> (merging branch into main)
    4) git push -u origin main (push new main with merged branch into main branch of remote repo)


#Other helpful git commands:
-) git status (check uncommitted changes and new files)
-) git branch (number of all branches and which on which branch currently)
-) git pull origin main (get latest version of remote main branch and merge it with local folder without overwriting new local changes)
-) git merge <branch_name> 
-) git clone https://github.com/sonnenbe-dot/GBAS-GUI.git (cloning my remote repo into local folder)
-) git branch -a (see all local and remote branches of the repository)
-) git switch --track origin/allele_determination_likelihoods (switching to the remote branch allele_determination_likelihoods and creating the local branch allele_determination_likelihoods as well)