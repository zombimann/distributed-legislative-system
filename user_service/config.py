#config.py

MYSQL_HOST = 'localhost'
MYSQL_USER = 'zombi'
MYSQL_PASSWORD = 'C0mpradors*'
MYSQL_DB = 'user_service_db'

# MySQL URI format: mysql://user:password@host/db_name
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# Set the secret key for JWT token generation
JWT_SECRET_KEY = 'your-secret-key-goes-here'
