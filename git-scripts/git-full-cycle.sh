source ./git-scripts/add-commit.sh "$1" &&
source ./venv/bin/activate
pip freeze > req.txt
source ./git-scripts/fetch-rebase-push.sh 
source ./git-scripts/tofork-fetch-rebase-push.sh