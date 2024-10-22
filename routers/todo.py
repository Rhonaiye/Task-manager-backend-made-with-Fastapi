from fastapi import APIRouter, Depends, status, HTTPException, Path
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Todo, Users
from passlib.context import CryptContext
from typing import Annotated
from pydantic import BaseModel, Field
from routers.auth import get_current_user, Usersreq
from fastapi.logger import logger
from fastapi.responses import JSONResponse  # Import for structured responses


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# Pydantic Model for Todo Request
class TodoReq(BaseModel):
    title: str
    description: str



# Helper function to serialize the Todo model
def serialize_todo(todo_model: Todo):
    return {
        "id": todo_model.id,
        "title": todo_model.title,
        "description": todo_model.description,
        "complete": todo_model.complete,
        "user_id": todo_model.user_id,
    }



@router.get('/get_todo', status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency):
    todos = db.query(Todo).all()
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Items not found')
    return [serialize_todo(todo) for todo in todos]




@router.get('/get-incomplete-todo/', status_code=status.HTTP_200_OK)
async def get_incomplete_tasks(db: db_dependency, current_user: Users = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.complete == False, Todo.user_id == current_user.id).all()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Items not found')
    return [serialize_todo(t) for t in todo]



@router.get('/get-todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: int, db: db_dependency):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No item matched')
    return serialize_todo(todo)



@router.get('/get-completed-todo/', status_code=status.HTTP_200_OK)
async def get_completed_tasks(db: db_dependency, current_user: Users = Depends(get_current_user)):
    completed_todo = db.query(Todo).filter(Todo.complete == True, Todo.user_id == current_user.id).all()
    if not completed_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No completed items found')
    return [serialize_todo(t) for t in completed_todo]




@router.post('/create-todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_req: TodoReq, current_user: Users = Depends(get_current_user)):
    logger.info(f"Received request to create todo: {todo_req}")
    todo_model = Todo(
        title=todo_req.title,
        description=todo_req.description,
        user_id=current_user.id,
    )
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)  # Refresh to get the latest data from the database
    return JSONResponse(content={"message": "Todo created successfully", "todo": serialize_todo(todo_model)}, status_code=status.HTTP_201_CREATED)




@router.delete('/delete-todo/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(todo_id: int, db: db_dependency):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    db.delete(todo)
    db.commit()
    return JSONResponse(content={"message": "Todo deleted successfully"}, status_code=status.HTTP_202_ACCEPTED)





@router.put('/update-todo/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_todo(todo_id: int, db: db_dependency, todo_req: TodoReq):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    db.commit()  # No need for add here, just commit the changes

    return JSONResponse(content={"message": "Todo updated successfully", "todo": serialize_todo(todo_model)}, status_code=status.HTTP_202_ACCEPTED)





@router.patch('/complete-task/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
async def complete_task(todo_id: int, db: db_dependency):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    if todo_model.complete:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Task already complete')

    todo_model.complete = True
    db.commit()  # No need for add here, just commit the changes

    return JSONResponse(content={"message": "Task marked as complete successfully"}, status_code=status.HTTP_202_ACCEPTED)
