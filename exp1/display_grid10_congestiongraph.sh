#!/bin/bash
cd code_directories

# Define the Python command to run
python_command="python3 graph_congestion_matrix.py grid_10 500"

# Open four terminal windows and execute the Python command in each
osascript -e 'tell application "Terminal" to do script "'"${python_command}"'"'
osascript -e 'tell application "Terminal" to do script "'"${python_command}"'"'
osascript -e 'tell application "Terminal" to do script "'"${python_command}"'"'
osascript -e 'tell application "Terminal" to do script "'"${python_command}"'"'
sleep 10