#!/bin/bash

set -e 
set -u

mkdir -p scripts

for CSV_FILE in test-data/*-abcd.csv.gz; do
  BASE_NAME=$(basename $CSV_FILE .csv.gz)
  CMND_NAME=`sed 's/data-test/test-01/g' <<<"$BASE_NAME"`
  printf "#!/bin/bash

set -e
set -u

FILE=%s

DST_DIR=../../../JeMPI/docker/docker_data/async_receiver/csv

pushd ../test-data
  rm -f \$DST_DIR/*.csv
  set -e
  gzip -d -k \$FILE.csv.gz    
  mv \$FILE.csv \$DST_DIR/\$FILE.temp
  mv \$DST_DIR/\$FILE.temp \$DST_DIR/\$FILE.csv
popd  
" $BASE_NAME > scripts/$CMND_NAME.sh
  chmod u+x scripts/$CMND_NAME.sh  
done  

