#!/bin/bash
cd /app/src
for f in $(find /inputs -maxdepth 1 -type f -printf "%f\n"); do
    python main_cli.py /inputs/$f /outputs/$f
done
