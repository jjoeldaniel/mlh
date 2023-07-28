#!/usr/bin/env bash

echo "Flask server starting"

cd ~/mlh
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

echo "Flask server successfully started"
