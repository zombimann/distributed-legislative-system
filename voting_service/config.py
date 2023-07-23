#config.py 

import os

MYSQL_HOST = 'localhost'
MYSQL_USER = 'zombi'
MYSQL_PASSWORD = 'C0mpradors*'
MYSQL_DB = 'voting_service_db'

SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
