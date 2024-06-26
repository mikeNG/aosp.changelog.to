#!/bin/bash

OLD_VERSION=$1
NEW_VERSION=$2
BASE_DIRECTORY=$3

GET_PROJECT_GITLOG="$BASE_DIRECTORY/get_project_gitlog.sh $OLD_VERSION $NEW_VERSION"
HTML_FORMATTER=$BASE_DIRECTORY/gitlog_to_html

OUTPUT_FILENAME=$OLD_VERSION-to-$NEW_VERSION.html

function renameTmp {
	rm $OUTPUT_FILENAME
	mv $OUTPUT_FILENAME.tmp $OUTPUT_FILENAME
}

cat $BASE_DIRECTORY/html_templates/header.html > $OUTPUT_FILENAME
sed "s/FROM_VERSION/$OLD_VERSION/g" $OUTPUT_FILENAME > $OUTPUT_FILENAME.tmp
renameTmp
sed "s/TO_VERSION/$NEW_VERSION/g" $OUTPUT_FILENAME > $OUTPUT_FILENAME.tmp
renameTmp
repo forall -c "$GET_PROJECT_GITLOG" | $HTML_FORMATTER >> $OUTPUT_FILENAME
cat $BASE_DIRECTORY/html_templates/footer.html >> $OUTPUT_FILENAME
