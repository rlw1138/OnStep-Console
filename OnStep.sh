#!/bin/bash -i
set +v
cd "/media/rlw1138/DATA/\!Documents\!/PYTHON/onstep-python-master/OnStep Console"

# force the terminal to 34 high x 81 across
printf '\e[8;34;81t'

python3 ./onstep_console.py

#read -p "hit Enter to exit to System"
