#!/bin/bash

APP_DIR="`dirname $0`"
IMAGE_TAG="${1:-text_sim}"

(cd $APP_DIR && docker build -t $IMAGE_TAG $APP_DIR && docker run -d -p 80:80 $IMAGE_TAG)