from fastapi import FastAPI
from routes import auth_routs, board_routs, list_routes, task_routes, ai_tasks
app = FastAPI()

app.include_router(auth_routs.router, prefix="/auth", tags=['Auth'])
app.include_router(board_routs.router, prefix="/boards", tags=['Boards'])
app.include_router(list_routes.router, prefix="/list", tags=["List"])
app.include_router(task_routes.router, prefix="/task", tags=['Tasks'])
app.include_router(ai_tasks.router, prefix="/AIP", tags=['AI-Feature'])

@app.get("/")
def root():
    return {"message":"Back end is running"}