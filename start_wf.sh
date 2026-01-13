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
  --title="Docker Compose" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; docker-compose up --build; exec zsh'" &

xfce4-terminal \
  --title="Posting CLI" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source .venv/bin/activate; posting; exec zsh'" &

flatpak run io.github.ppvan.tarug &
