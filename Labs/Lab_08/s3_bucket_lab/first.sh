#!/bin/bash

set -e

FILE=$1
BUCKET=$2
EXPIRE=$3

FILENAME=$(basename "$FILE")

aws s3 mb s3://$BUCKET

aws s3 cp "$FILE" s3://$BUCKET/$FILENAME

url=$(aws s3 presign --expires-in $EXPIRE s3://$BUCKET/"$FILENAME")

echo "$url"
