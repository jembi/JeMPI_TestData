#!/bin/bash

set -e 
set -u

mkdir -p scripts

for CSV_FILE in test-data/*-dcab.csv.gz; do
  BASE_NAME=$(basename $CSV_FILE .csv.gz)
  CMND_NAME=`sed 's/data-test/test-01/g' <<<"$BASE_NAME-0-jenkins"`
  printf "#!/bin/bash

set -e
set -u

FILE=%s

DST_DIR=../../../jempi/docker/docker_data/data-apps/async_receiver/csv

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

