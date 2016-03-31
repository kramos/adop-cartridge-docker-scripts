#!/bin/bash
BASE_DIR="/var/tmp/"
PORT_FILE="${BASE_DIR}ports.txt"
PROCESS_FILE="${BASE_DIR}processes.txt"

# check expected ports are open
for p in $(cat ${PORT_FILE}); do
  if $(nc -z localhost $p); then
    echo "+ expected port open: $p"
  else
    echo "- expected port closed: $p"
  fi
done

## check for unexpected open ports
#for i in {1..65535}; do
#  cat ${PORT_FILE} | grep "$i" >/dev/null
#  if [ $? -eq 1 ]; then
#    if $(nc -z localhost $i); then
#      echo "- unexpected port open $i"
#    fi
#  fi
#done

# check for expected processes
while read f
do

  echo $f | grep "^###" >/dev/null
  if [ $? -eq 0 ]; then
    continue
  fi

  owner=$(echo $f | awk '{print $1}')
  process=$(echo $f | awk '{$1 = ""; print $0; }')

  ps -ef | grep -v grep | grep "${process}" >/dev/null
  if [ $? -eq 0 ]; then
    echo "+ expected process found: ${process}"

    ps -ef | grep -v grep | grep "${process}" | awk '{print $1}' | grep "${owner}" >/dev/null
    if [ $? -eq 0 ]; then
      echo "+ expected process owner: ${owner}"
    else
      echo "- expected process incorrect owner: ${owner} /${process}"
    fi

  else
    echo "- expected process missing: ${owner} /${process}"
  fi

done < ${PROCESS_FILE}

# check for unexpected processes
ps -ef | while read p2
do
  flag=1
  echo $p2 | grep "^UID" >/dev/null
  if [ $? -eq 1 ]; then
    owner2=$(echo $p2 | awk '{print $1}')
    process2=$(echo $p2 | awk '{$2 = ""; $3 = ""; $4 = ""; $5 = ""; $6 = ""; $7 = ""; print $0; }')

    cat ${PROCESS_FILE} | ( while read p3
    do
      owner3=$(echo $p3 | awk '{print $1}')
      process3=$(echo $p3 | awk '{$1 = ""; print $0; }')

      echo "${process2}" | grep "${process3}" >/dev/null
      if [ $? -eq 0 ]; then
        flag=0
        break
      fi
    done
    if [ $flag -eq 1 ]; then
      echo "- unexpected process found: $p2"
    fi )

  fi
done
