from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.list_model import create_list, get_lists

router = APIRouter()

class Lists(BaseModel):
    board_id : int
    name : str
    position : int

@router.post("/lists")
def add_list(list_in: Lists):
    try:
        success = create_list(list_in.board_id, list_in.name, list_in.position)
        if not success:
            raise HTTPException(status_code=400, detail=f"failed to add the list")
        return {"message": "List is created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")
    
@router.get("/lists/{board_id}")
def fetch_lists(board_id: int):
    try:
        lists = get_lists(board_id)
        return {"lists":lists}
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")