#!/bin/bash

ZIP_FILE_NAME=ratings-service-lambda.zip
S3_LOCATION=spoon-feed-dev/lambda-functions/$ZIP_FILE_NAME

aws s3 cp $ZIP_FILE_NAME s3://$S3_LOCATION
