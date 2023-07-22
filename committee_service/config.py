MYSQL_HOST = 'localhost'
MYSQL_USER = 'zombi'
MYSQL_PASSWORD = 'C0mpradors*'
MYSQL_DB = 'committee_service_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
