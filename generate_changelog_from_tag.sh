#!/bin/bash

PARENT_TAG=$1
TARGET_TAG=$2
AOSP_DIRECTORY=$3

BASE_DIRECTORY=$AOSP_DIRECTORY/../aosp.changelog.to
WORK_DIRECTORY=$AOSP_DIRECTORY/build/make
cd $WORK_DIRECTORY

echo "Generating changelog from $PARENT_TAG to $TARGET_TAG"

# Enter the AOSP working directory
cd $AOSP_DIRECTORY

$BASE_DIRECTORY/get_gitlog.sh $PARENT_TAG $TARGET_TAG $BASE_DIRECTORY
