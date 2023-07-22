# config.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'zombi'
MYSQL_PASSWORD = 'C0mpradors*'
MYSQL_DB = 'bills_service_db'
SECRET_KEY = 'your_secret_key_here'
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
