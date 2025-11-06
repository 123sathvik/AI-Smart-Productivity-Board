from fastapi import APIRouter, HTTPException
from utils.db import get_connection
from AI.ai_prediction import ai_predict
from pymysql import MySQLError
import json
from pydantic import BaseModel

router = APIRouter()


def get_task(task_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select id,title, description from tasks where id=%s", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"id": row["id"], "title": row["title"], "description": row["description"]}
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


@router.post("/priority/{task_id}")
async def predict_priority(task_id: int):
    task = get_task(task_id)

    s_prompt = f"You are an AI that classifies task priority as Low, Medium, or High. Consider title and the description for prediction.: {task['title']} - {task['description']}"

    ai_response = await ai_predict(s_prompt)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET category=%s WHERE id=%s", (ai_response, task_id))
        conn.commit()
        return {"task_id": task_id, "priority": ai_response}
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error updating priority: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/category/{task_id}")
async def predict_category(task_id:int):
    task = get_task(task_id)
    prompt = f"You are an AI that classifies tasks into categories (Work, Study, Personal, Health, etc.). Consider title and the description for prediction. Task: {task['title']} - {task['description']}"
    ai_response = await ai_predict(prompt)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "update tasks set category = %s where id=%s",(ai_response, task_id))
        conn.commit()
        return {"task_id": task_id, "category": ai_response}
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error updating category: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/deadline/{task_id}")
async def predict_deadline(task_id: int):
    task = get_task(task_id)
    prompt = f"You are an AI that predicts a reasonable due date (in YYYY-MM-DD format) for a given task. Consider title and the description for prediction. Task: {task['title']} - {task['description']}"
    ai_response = await ai_predict(prompt)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET due_date=%s WHERE id=%s", (ai_response, task_id))
        conn.commit()
        return {"task_id": task_id, "due_date": ai_response}
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error updating due date: {str(e)}")
    finally:
        cursor.close()
        conn.close()



@router.post("/subtasks/{task_id}")
async def generate_subtasks(task_id:int):
    task = get_task(task_id)
    prompt = f"You are an AI that breaks down a task description into smaller subtasks. display with serialize nnumbers include small information about the subtask also (return as json list of strings): {task['title']} - {task['description']}"
    ai_response = await ai_predict(prompt)

    try:
        subtasks = json.loads(ai_response)
    except Exception:
        subtasks = [line.strip("-• ")   for line in ai_response.split("\n") if line.strip]

    return {"task_id": task_id, "subtasks": subtasks}
