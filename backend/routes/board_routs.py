from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.board_model import create_board, get_boards

router = APIRouter()

class Board(BaseModel):
    name : str
    owner_id : int

@router.post("/board")
def add_board(board: Board):
    try:
        success = create_board(board.name, board.owner_id)
        if not success:
            raise HTTPException(status_code=400, detail="failed to create a board")
        return {"message" : "Board created successfullu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.get("/board/{owner_id}")
def list_board(owner_id: int):
    try:
        boards = get_boards(owner_id)
        return {"boards": boards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"internal server error: {str(e)}")
    
