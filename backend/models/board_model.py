from utils.db import get_connection

def create_board(name: str, owner_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "insert into boards(name, owner_id) values(%s,%s)",(name, owner_id)
        )
        conn.commit()
        return True
    except Exception as e:
        raise Exception(f"Dayabase error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def get_boards(owner_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "select board_id, name from boards where owner_id = %s",(owner_id,)
        )
        boards = cursor.fetchall()
        return boards
    except Exception as e:
        raise Exception(f"error in fetching {str(e)}")
    finally:
        cursor.close()
        conn.close()
        
