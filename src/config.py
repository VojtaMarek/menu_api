import os


DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'menu_api')
DB_USER = os.getenv('DB_USER', 'user_name')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
# DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_URL = 'sqlite:///menu_api.db'  # set this as the environment variable
