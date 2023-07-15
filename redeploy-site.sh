#!/usr/bin/env bash

echo "Flask server starting"

tmux kill-server
cd $HOME/projects/mlh_port
git fetch && git reset origin/main --hard
tmux new -d -s flask_temp
tmux send-keys -t flask "source venv/bin/activate.fish && pip install -r requirements.txt" ENTER
cd ./

tmux kill-server
systemctl restart myportfolio

echo "Flask server successfully started"
