#!/bin/bash

ZIP_FILE_NAME=ratings-service-lambda.zip
ZIP_FILE_LOCATION=~/$ZIP_FILE_NAME
S3_LOCATION=spoon-feed-dev/lambda-functions/$ZIP_FILE_NAME

aws s3 cp $ZIP_FILE_LOCATION s3://$S3_LOCATION
