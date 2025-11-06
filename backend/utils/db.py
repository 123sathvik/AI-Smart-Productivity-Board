
import pymysql
from db.config import DB_config

def get_connection():
    try:
        conn = pymysql.connect(
            host=DB_config["host"],
            user=DB_config["user"],
            password=DB_config["password"],
            database=DB_config["database"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")
