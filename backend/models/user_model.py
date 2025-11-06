from utils.db import get_connection
import bcrypt

#signup
def create_user(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    hash_pas = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    try:
        cursor.execute(
            "insert into users(email, password) values(%s,%s )",
            (email, hash_pas.decode('utf-8'))
        )
        conn.commit()
        return True
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

#login
def log_user(email:str, password:str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "select * from users where email= %s",(email,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return True
    return False
    