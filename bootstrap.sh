#!/usr/bin/env bash
rm -rf devops-env
python2 -m virtualenv devops-env
source devops-env/bin/activate
unset PYTHONPATH
python2 -m pip install -r requirements.txt
#echo "----- Created venv -------"