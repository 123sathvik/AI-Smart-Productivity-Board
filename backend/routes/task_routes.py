from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.task_model import create_task,get_task_by_list,update_task, delete_task

router = APIRouter()

class Task(BaseModel):
    list_id : int
    title : str
    description: str=None
    category : str = None
    due_date : str =None

@router.post("/tasks")
def add_task(task: Task):
    try:
        result = create_task(
            list_id=task.list_id,
            title=task.title,
            description=task.description,
            category=task.category,
            due_date=task.due_date
        )
        if not result:
            raise HTTPException(status_code=400, detail="Error creating task")
        return {"message": "Task is created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")

@router.get("/tasks/{list_id}")
def get_tasks(list_id: int):
    try:
        tasks = get_task_by_list(list_id)
        return {"tasks": tasks}
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")
    
@router.patch("/tasks/{task_id}")
def edit_task(task_id:int, updates: dict):
    try:
        result = update_task(task_id, updates)
        if not result:
            raise HTTPException(status_code=400, detail="Error updating task")
        return {"message": "Task updated successfully"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")

@router.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    result = delete_task(task_id)
    if not result:
        if not result:
            raise HTTPException(status_code=400, detail="Error deleting task")
        return {"message": "task is deleted"}