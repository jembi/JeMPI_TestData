#!/bin/bash

set -e 
set -u

mkdir -p scripts

for CSV_FILE in test-data/*-abcd.csv.gz; do
  FULL_NAME=$(basename $CSV_FILE .csv.gz)                               
  BASE_NAME=$(sed s/-abcd// <<<$FULL_NAME)
  CMND_NAME=`sed 's/data-test/test-01/g' <<<"$BASE_NAME"`

  printf "#!/bin/bash

set -e
set -u

FILE=%s

DST_DIR=../../../JeMPI/docker/docker_data/data-apps/test_01/csv

pushd ../test-data
  rm -f \$DST_DIR/*.csv
  set -e
  gzip -d -k \$FILE-abcd.csv.gz
  sed 1,1d \$FILE-abcd.csv | shuf >\$DST_DIR/\$FILE-dcab.temp
  HEADER=\`head -1 \$FILE-abcd.csv\`
  sed -i '1i '\$HEADER \$DST_DIR/\$FILE-dcab.temp
  rm \$FILE-abcd.csv
  mv \$DST_DIR/\$FILE-dcab.temp \$DST_DIR/\$FILE-dcab.csv
popd
" $BASE_NAME > scripts/$CMND_NAME-dcab-1.sh
  chmod u+x scripts/$CMND_NAME-dcab-1.sh
done  

