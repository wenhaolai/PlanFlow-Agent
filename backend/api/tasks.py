from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.mysql import get_db
from services.UserService import get_current_user
from models.UserModel import User
from models.TasksModel import Task
from schemas.TaskSchema import TaskResponse, TaskDetailResponse

router = APIRouter()

@router.get("/task/gettasklist", response_model=List[TaskResponse])
async def get_task_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).order_by(Task.updated_at.desc()).all()
    return tasks


@router.get("/task/{task_id}", response_model=TaskDetailResponse)
async def get_task_detail(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    print(f"in get_task_detail, search task_id={task_id}, get task={task}")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task