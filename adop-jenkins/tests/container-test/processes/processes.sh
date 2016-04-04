#!/bin/bash
BASE_DIR=$1
NAME=$2
CFG_FILE=${BASE_DIR}/${NAME}/${NAME}.cfg

echo "# Starting process tests"

# check for expected processes
while read f
do

  echo $f | grep "^#" >/dev/null
  if [ $? -eq 0 ]; then
    continue
  fi

  owner=$(echo $f | awk '{print $1}')
  process=$(echo $f | awk '{$1 = ""; print $0; }')
  eval_process=$(echo $(eval "echo $process"))

  ps -ef | grep -v grep | grep "${eval_process}" >/dev/null
  if [ $? -eq 0 ]; then
    echo "+ expected process found: ${eval_process}"

    ps -ef | grep -v grep | grep "${eval_process}" | awk '{print $1}' | grep "${owner}" >/dev/null
    if [ $? -eq 0 ]; then
      echo "+ expected process owner: ${owner}"
    else
      echo "- expected process incorrect owner: ${owner} /${eval_process}"
    fi

  else
    echo "- expected process missing: ${owner} /${eval_process}"
  fi

done < ${CFG_FILE}

# check for unexpected processes
ps -ef | while read p
do
  flag=1
  echo $p | grep "^UID" >/dev/null
  if [ $? -eq 1 ]; then
    owner2=$(echo $p | awk '{print $1}')
    process2=$(echo $p | awk '{$2 = ""; $3 = ""; $4 = ""; $5 = ""; $6 = ""; $7 = ""; print $0; }')

    cat ${CFG_FILE} | ( while read p2
    do
      owner3=$(echo $p2 | awk '{print $1}')
      process3=$(echo $p2 | awk '{$1 = ""; print $0; }')
      eval_process3=$(echo $(eval "echo $process3"))

      echo "${process2}" | grep "${eval_process3}" >/dev/null
      if [ $? -eq 0 ]; then
        flag=0
        break
      fi
    done
    if [ $flag -eq 1 ]; then
      echo "- unexpected process found: $p"
    fi )

  fi
done

echo "# Finished process tests"
