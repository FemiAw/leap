#!/bin/bash

pip install --editable .
export FLASK_APP=leap
flask run
