from utils.db import get_connection

def create_list(board_id: int, name: str, position: int):
    conn = get_connection()
    if conn is None:
        print("db connection failed in create list")
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "insert into lists(board_id, name, position) values (%s,%s,%s)",(board_id, name, position)
        )
        conn.commit()
        return True
    except Exception as e:
        raise Exception(f"Dayabase error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def get_lists(board_id: int):
    conn = get_connection()
    if conn is None:
        print("db connectiob failed in get_lists")
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("select * from lists where board_id =%s order by position", (board_id,))
        listss = cursor.fetchall()
        return listss
    except Exception as e:
        raise Exception(f"error in fetching {str(e)}")
    finally:
        cursor.close()
        conn.close()