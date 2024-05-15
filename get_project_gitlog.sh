#!/bin/sh

OLD_VERSION=$1
NEW_VERSION=$2

grep projectname .git/config ;
if git rev-parse ${OLD_VERSION} >/dev/null 2>&1
then
git log --oneline --no-merges ${OLD_VERSION}..${NEW_VERSION}
else
git log --oneline --no-merges ${NEW_VERSION}
fi
