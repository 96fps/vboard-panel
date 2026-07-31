#!/bin/bash

pkill  -f "python3 ./vboard.py"
pkill  -f "python3 ./vboard_nav.py"
pkill  -f "python3 ./vboard_fn.py"

bash -c 'python3 ./vboard_fn.py'
