#!/bin/bash
BASE_DIR=$(pwd)
PORTS="ports"
PROCESSES="processes"

# run port checks
${BASE_DIR}/${PORTS}/${PORTS}.sh ${PORTS}

# run process checks
${BASE_DIR}/${PROCESSES}/${PROCESSES}.sh ${PROCESSES}
