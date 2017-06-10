#! /bin/bash

ZIP_FILE_LOCATION=~/ratings-service-lambda.zip
VIRTUAL_ENV_DIR=/tmp/venv

if [ -d "$VIRTUAL_ENV_DIR" ]; then
  rm -rf $VIRTUAL_ENV_DIR
fi

if [ -f "$ZIP_FILE_LOCATION" ]; then
  rm $ZIP_FILE_LOCATION
fi

echo "Creating virtual environment..."
virtualenv -p python3 $VIRTUAL_ENV_DIR
source $VIRTUAL_ENV_DIR/bin/activate
echo "Installing Python packages..."
pip install neo4j-driver
echo "Zipping up Python packages..."
cd $VIRTUAL_ENV_DIR/lib/python3.6/site-packages/
zip -r9 $ZIP_FILE_LOCATION *
echo "Zipping up lambda functions..."
cd - 
zip -g $ZIP_FILE_LOCATION *.py
deactivate