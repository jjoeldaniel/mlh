#!/usr/bin/env bash

tmux kill-server
tmux new -d -s flask
tmux send-keys -t flask "cd ./projects/mlh_port" ENTER
tmux send-keys -t flask "git fetch && git reset origin/main --hard" ENTER
tmux send-keys -t flask "source venv/bin/activate.fish && pip install -r requirements.txt" ENTER
tmux send-keys -t flask "python3 -m flask run -h 0.0.0.0" ENTER

echo "Flask server successfully started"
