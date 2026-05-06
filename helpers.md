

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



#Other helpful git commands:
-) git status (check uncommitted changes and new files)
-) git branch (number of all branches and which on which branch currently)