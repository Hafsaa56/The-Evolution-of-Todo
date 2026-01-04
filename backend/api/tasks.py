import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List
import uuid
from database import get_session
from models.task import Task, TaskBase
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from middleware.auth import get_current_user
from utils.logging import get_logger
from utils.validation import validate_title, validate_description

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user.
    """
    logger.info(f"Fetching tasks for user: {current_user.id}")
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.id)
    ).all()
    logger.info(f"Retrieved {len(tasks)} tasks for user: {current_user.id}")
    return tasks

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user.
    """
    # Validate title
    is_valid, error = validate_title(task.title)
    if not is_valid:
        logger.warning(f"Title validation failed for user: {current_user.id}, error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    # Validate description
    is_valid, error = validate_description(task.description)
    if not is_valid:
        logger.warning(f"Description validation failed for user: {current_user.id}, error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    logger.info(f"Creating new task for user: {current_user.id}, title: {task.title}")
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Task created successfully with ID: {db_task.id}")
    return db_task

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    """
    logger.info(f"Fetching task ID: {task_id} for user: {current_user.id}")
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id} for user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        logger.warning(f"Unauthorized access attempt to task: {task_id} by user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    logger.info(f"Task retrieved successfully: {task_id}")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.
    """
    logger.info(f"Updating task ID: {task_id} for user: {current_user.id}")
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found for update: {task_id} for user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        logger.warning(f"Unauthorized update attempt to task: {task_id} by user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Validate title if provided
    if task_update.title is not None:
        is_valid, error = validate_title(task_update.title)
        if not is_valid:
            logger.warning(f"Title validation failed for user: {current_user.id}, error: {error}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )

    # Validate description if provided
    if task_update.description is not None:
        is_valid, error = validate_description(task_update.description)
        if not is_valid:
            logger.warning(f"Description validation failed for user: {current_user.id}, error: {error}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )

    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    logger.info(f"Task updated successfully: {task_id}")
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.
    """
    logger.info(f"Deleting task ID: {task_id} for user: {current_user.id}")
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found for deletion: {task_id} for user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        logger.warning(f"Unauthorized deletion attempt to task: {task_id} by user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()
    logger.info(f"Task deleted successfully: {task_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_completion(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    """
    logger.info(f"Toggling completion for task ID: {task_id} for user: {current_user.id}")
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found for toggle: {task_id} for user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        logger.warning(f"Unauthorized toggle attempt to task: {task_id} by user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Toggle completion status
    old_completed = task.completed
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    logger.info(f"Task completion toggled successfully: {task_id} (from {old_completed} to {task.completed})")
    return task