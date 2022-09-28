#!/bin/bash

set -e
set -a

shopt -s nullglob
fileNameRegex="config-test-[0-9]*-[a-d]-[0-9]*-[0-9]*.json"
for f in *.json; do
  [[ $f =~ $fileNameRegex ]] && python generate-data.py $f
done  
