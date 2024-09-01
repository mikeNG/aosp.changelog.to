#!/bin/bash

PARENT_TAG=$1
TARGET_TAG=$2
AOSP_DIRECTORY=$3

BASE_DIRECTORY=$AOSP_DIRECTORY/../aosp.changelog.to
PUBLISH_DIRECTORY=$BASE_DIRECTORY/../gh-pages

echo "Generating changelog from $PARENT_TAG to $TARGET_TAG"

# Enter the AOSP working directory
cd $AOSP_DIRECTORY

$BASE_DIRECTORY/get_gitlog.sh $PARENT_TAG $TARGET_TAG $BASE_DIRECTORY

if [ -d "$PUBLISH_DIRECTORY" ]; then
    mv "$PARENT_TAG"-to-"$TARGET_TAG".html "$PUBLISH_DIRECTORY"
fi
