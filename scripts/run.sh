#!/bin/bash

IMAGE='my_image'
WORKDIR=$(pwd)
USER=$UID
GROUP=${GROUPS[0]}
RM='true'

docker run -it --rm=${RM} \
  -v ${WORKDIR}:/home/working \
  -u="${USER}:${GROUP}" \
  -w="/home/working" \
  ${IMAGE} \
  && $1
