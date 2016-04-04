#!/bin/bash
BASE_DIR=$1
PORTS="ports"
PROCESSES="processes"

# run port checks
${BASE_DIR}/${PORTS}/${PORTS}.sh ${BASE_DIR} ${PORTS}

# run process checks
${BASE_DIR}/${PROCESSES}/${PROCESSES}.sh ${BASE_DIR} ${PROCESSES}
