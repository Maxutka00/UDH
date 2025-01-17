#!/bin/bash

export DB_NAME="udh_backend"
export DB_USER="udh_backend_admin"
export DB_USER_PASSWORD="4tm8RSmTY3x3"
export DB_HOST="54.37.74.248"
export DB_PORT="5444"

#source venv/Scripts/activate
python udh_backend/manage.py runserver