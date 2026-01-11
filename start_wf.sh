#!/bin/bash

BASE_DIR="/home/andriomdac/autoservice-api"

xfce4-terminal \
  --title="API Shell" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; exec zsh'" &

xfce4-terminal \
  --title="API Neovim" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; nvim .'" &

xfce4-terminal \
  --title="FastAPI Server" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; fastapi dev app.py; exec zsh'" &

xfce4-terminal \
  --title="Posting CLI" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; posting; exec zsh'" &

xfce4-terminal \
  --title="SQLite CLI" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; sqlit; exec zsh'" &
