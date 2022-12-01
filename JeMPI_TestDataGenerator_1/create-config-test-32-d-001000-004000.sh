#!/bin/bash

set -e
set -a

DATA_DIR=./test-data

shopt -s nullglob

function generate() {
  python generate-data.py $1 
  for SRC in $DATA_DIR/*-abcd.csv; do
    DST=`sed 's/abcd/dcab/g' <<<"$SRC"`
    sed 1,1d $SRC | shuf >$DST
    HEADER=`head -1 $SRC`
    sed -i '1i '$HEADER $DST
  done
  gzip $DATA_DIR/*.csv
}


[[ -d $DATA_DIR ]] && rm -r $DATA_DIR
mkdir -p $DATA_DIR

# fileNameRegex="config-test-[0-9]*-[a-d]-[0-9]*-[0-9]*.json"
# for f in *.json; do
#   [[ $f =~ $fileNameRegex ]] && generate $f
# done  

generate config-test-32-d-001000-004000.json
