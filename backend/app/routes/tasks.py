from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas, utils

router = APIRouter(prefix="/tasks", tags=["tasks"])

# -------- CREATE TASK --------
@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    db_task = models.Task(**task.dict(), owner=current_user)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# -------- COMPLETE TASK --------
@router.put("/{task_id}/complete", response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    db.commit()
    db.refresh(task)
    return task

# -------- LIST TASKS --------
@router.get("/", response_model=list[schemas.TaskResponse])
def list_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

# -------- DELETE TASK --------
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}

# -------- UPDATE TASK --------
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task

# -------- TOGGLE COMPLETION --------
@router.patch("/{task_id}/toggle", response_model=schemas.TaskResponse)
def toggle_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(utils.get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.completed = not db_task.completed
    db.commit()
    db.refresh(db_task)
    return db_task
