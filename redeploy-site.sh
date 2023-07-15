#!/usr/bin/env bash

echo "Flask server starting"

tmux kill-server
tmux new -d -s flask_temp
tmux send-keys -t flask "cd $HOME/projects/mlh_port" ENTER
tmux send-keys -t flask "git fetch && git reset origin/main --hard" ENTER
tmux send-keys -t flask "source venv/bin/activate.fish && pip install -r requirements.txt" ENTER
tmux kill-server

systemctl restart myportfolio

echo "Flask server successfully started"
