#!/bin/bash
# Entry point for the container. First arg is mode: master, worker, history.

MODE=$1

if [ "$MODE" = "master" ]; then
  ${SPARK_HOME}/sbin/start-master.sh
  tail -f ${SPARK_HOME}/logs/*

elif [ "$MODE" = "worker" ]; then
  # SPARK_MASTER_URL must be passed via env
  if [ -z "${SPARK_MASTER_URL}" ]; then
    echo "Error: SPARK_MASTER_URL not set for worker"
    exit 1
  fi
  ${SPARK_HOME}/sbin/start-worker.sh ${SPARK_MASTER_URL}
  tail -f ${SPARK_HOME}/logs/*

elif [ "$MODE" = "history" ]; then
  ${SPARK_HOME}/sbin/start-history-server.sh
  tail -f ${SPARK_HOME}/logs/*

else
  echo "Unknown mode: $MODE"
  exit 1
fi
