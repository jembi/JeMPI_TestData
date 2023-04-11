#!/bin/bash

set -e
set -u

THRESHOLD=$1

get_seeded_random()
{
  seed="$1"
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}

FILE=synthetic_data_kenya_V000
DST_DIR=../../JeMPI/docker/docker_data/data-apps/async_receiver/csv

sed 1,1d ./Results/$FILE.csv | shuf --random-source=<(get_seeded_random 42) >$DST_DIR/$FILE.temp
HEADER=`head -1 ./Results/$FILE.csv`
sed -i '1i '$HEADER $DST_DIR/$FILE.temp
rm -f $DST_DIR/$FILE.csv
mv $DST_DIR/$FILE.temp $DST_DIR/${FILE}_gn_S_fn_S_th_${THRESHOLD}.csv

