#!/bin/bash

set -e
set -u

FILE=synthetic_data_kenya_V000
DST_DIR=../../JeMPI/docker/docker_data/data-apps/async_receiver/csv

sed 1,1d ./Results/$FILE.csv | shuf >$DST_DIR/$FILE.temp
HEADER=`head -1 ./Results/$FILE.csv`
sed -i '1i '$HEADER $DST_DIR/$FILE.temp
rm -f $DST_DIR/$FILE.csv
mv $DST_DIR/$FILE.temp $DST_DIR/$FILE.csv

