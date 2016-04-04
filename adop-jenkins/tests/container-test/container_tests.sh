#!/bin/bash
BASE_DIR=$1
PORTS="ports"
PROCESSES="processes"

echo "# Starting container tests"

# run port checks
${BASE_DIR}/${PORTS}/${PORTS}.sh ${BASE_DIR} ${PORTS}

# run process checks
${BASE_DIR}/${PROCESSES}/${PROCESSES}.sh ${BASE_DIR} ${PROCESSES}

echo "# Finished container tests"
