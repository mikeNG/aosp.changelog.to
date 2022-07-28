#!/bin/bash

PARENT_TAG=$1
TARGET_TAG=$2
AOSP_DIRECTORY=$3

WORK_DIRECTORY=$AOSP_DIRECTORY/build/make
cd $WORK_DIRECTORY

echo "Generating changelog from $PARENT_TAG to $TARGET_TAG"

# Enter the AOSP working directory
cd $AOSP_DIRECTORY

$WORK_DIRECTORY/../aosp.changelog.to/get_gitlog.sh $PARENT_TAG $TARGET_TAG
