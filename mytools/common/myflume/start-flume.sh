#!/usr/bin/env bash


FLUME_CONF_DIR=${FLUME_CONF_DIR:-/opt/flume/conf}

[[ -z "${FLUME_CONF_FILE}"  ]] && { echo "FLUME_CONF_FILE required";  exit 1; }
[[ -z "${FLUME_AGENT_NAME}" ]] && { echo "FLUME_AGENT_NAME required"; exit 1; }

echo "Starting flume agent : ${FLUME_AGENT_NAME}"

flume-ng agent \
  -c ${FLUME_CONF_DIR} \
  -f ${FLUME_CONF_FILE} \
  -n ${FLUME_AGENT_NAME} \
  -Dflume.root.logger=INFO,console
