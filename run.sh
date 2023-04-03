#!/usr/bin/env bash

set -a
source .env
set +a

nohup python3.10 main.py &