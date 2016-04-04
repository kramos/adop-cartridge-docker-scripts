#!/bin/bash
BASE_DIR=$(echo ${TEST_DIR})
PORTS="ports"
PROCESSES="processes"

# run port checks
${BASE_DIR}/${PORTS}/${PORTS}.sh ${BASE_DIR} ${PORTS}

# run process checks
${BASE_DIR}/${PROCESSES}/${PROCESSES}.sh ${BASE_DIR} ${PROCESSES}
