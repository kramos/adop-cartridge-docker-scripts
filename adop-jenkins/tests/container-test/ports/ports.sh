#!/bin/bash
BASE_DIR=$1
NAME=$2
CFG_FILE=${BASE_DIR}/${NAME}/${NAME}.cfg

echo "# Starting port tests"

# check expected ports are open
for p in $(cat ${CFG_FILE}); do

  echo $p | grep "^#" >/dev/null
  if [ $? -eq 0 ]; then
    continue
  fi

  if $(nc -z localhost $p); then
    echo "+ expected port open: $p"
  else
    echo "- expected port closed: $p"
  fi
done

## check for unexpected open ports
#for i in {1..65535}; do
#  cat ${CFG_FILE} | grep "$i" >/dev/null
#  if [ $? -eq 1 ]; then
#    if $(nc -z localhost $i); then
#      echo "- unexpected port open $i"
#    fi
#  fi
#done

echo "# Finished port tests"
