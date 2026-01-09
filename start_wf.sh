#! /bin/bash

konsole --new-tab --noclose -e zsh -c "cd /home/andriomdac/Desktop/autoservice-api/ && source .venv/bin/activate && zsh" &
konsole --new-tab -e zsh -c "cd /home/andriomdac/Desktop/autoservice-api/ && source .venv/bin/activate && nvim ." &
konsole --new-tab --noclose -e zsh -c "cd /home/andriomdac/Desktop/autoservice-api/ && source .venv/bin/activate && fastapi dev app.py" &
konsole --new-tab --noclose -e zsh -c "cd /home/andriomdac/Desktop/autoservice-api/ && source .venv/bin/activate && posting" &
konsole --new-tab --noclose -e zsh -c "cd /home/andriomdac/Desktop/autoservice-api/ && source .venv/bin/activate && sqlit" &
