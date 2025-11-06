from utils.db import get_connection
from pymysql.err import MySQLError

def create_task(list_id:int, title:str, description: str =None, category: str=None, due_date: str =None):
    conn = get_connection()
    if conn is None:
        print("Connection failed")
    cursor = conn.cursor()
    try:
        query = """insert into tasks(list_id, title, description, category, due_date)values(%s,%s,%s,%s,%s)"""
        cursor.execute(query, (list_id, title, description, category,due_date)) 
        conn.commit()

        return {"id": cursor.lastrowid, "message": "Task creted successfully"}
    except MySQLError as e:
        raise Exception (f"error while creating: {str(e)}") from e
    finally:
        cursor.close()
        conn.close()

def get_task_by_list(list_id : int):
    conn = get_connection()
    if conn is None:
        print("Connection failed")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "select * from tasks where list_id=%s",(list_id,))
        tasks = cursor.fetchall()
        return tasks
    except MySQLError as e:
        raise Exception(f"error in getting task: {str(e)}") from e
    finally :
        cursor.close()
        conn.close()

def update_task(task_id: int, updates: dict):
    conn = get_connection()
    if conn is None:
        print("Connection failed")
    cursor = conn.cursor()
    try:
        fields = []
        values = []
        for key, value in updates.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(task_id)
        query = f"update tasks SET {', '.join(fields)} where id=%s"
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.rowcount>0
    except MySQLError as e:
        raise Exception(f"error in getting task: {str(e)}") from e
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "delete from tasks where id=%s",(task_id))
        return cursor.rowcount > 0
    except MySQLError as e:
        raise Exception(f"error in deletung : {str(e)}") from e
    finally:
        cursor.close()
        conn.close()

    