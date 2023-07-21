#!/usr/bin/env bash

echo "Flask server starting"

cd $HOME/projects/mlh_port
git fetch && git reset origin/main --hard
source venv/bin/activate && pip install -r requirements.txt

systemctl restart myportfolio

echo "Flask server successfully started"
