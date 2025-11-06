from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.user_model import create_user, log_user

router = APIRouter()

class Users(BaseModel):
    email : str
    password : str

#signup route
@router.post("/signup")
def signup(users: Users):
    try:
        success = create_user(users.email, users.password)
        if not success:
            raise HTTPException(status_code = 400, detail="user alrwady exist or some error please try again")
        else:
            return {"message": "registerd successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
#Login
@router.post("/login")
def login(users:Users):
    if log_user(users.email, users.password):
        return {"message": "Login successfull"}
    raise HTTPException(status_code = 400, detail= "Invalid")
