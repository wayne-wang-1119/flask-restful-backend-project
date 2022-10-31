#!/bin/bash

LOG_FILE=${PROJ_WS}/start.log

cd $PROJ_WS

git --version | tee -a ${LOG_FILE}
git clone https://samuel_yang0129%40msn.com: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@github.com/SamuelYang0129/$PROJ_NAME.git
cd $FLASK_APP_WS
git fetch --all
git checkout -b $DEMO_NAME origin/$DEMO_NAME

pip install -r requirements.txt

export FLASK_APP=entrypoint.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=5000
