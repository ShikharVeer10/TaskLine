"""
Task management endpoints.

POST   /tasks/         →  Create a new task
GET    /tasks/         →  List all your tasks
GET    /tasks/{id}     →  Get a specific task
PATCH  /tasks/{id}     →  Update a task
DELETE /tasks/{id}     →  Delete a task
"""
import uuid

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, func, col

from app import crud
from app.api.deps import SessionDep, CurrentUser
from app.models import (
    Task,
    TaskCreate,
    TaskPublic,
    TasksPublic,
    TaskUpdate,
    Message,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskPublic)
def create_task(
    *, session: SessionDep, current_user: CurrentUser, task_in: TaskCreate
) -> Task:
    """
    Create a new task.
    
    The task is automatically assigned to the logged-in user.
    Requires authentication.
    """
    task = crud.create_task(
        session=session, task_create=task_in, owner_id=current_user.id
    )
    return task


@router.get("/", response_model=TasksPublic)
def read_tasks(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> TasksPublic:
    """
    List all tasks belonging to the current user.
    
    Supports pagination with skip and limit.
    Requires authentication.
    """
    # Count total tasks for this user
    count_statement = (
        select(func.count())
        .select_from(Task)
        .where(Task.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    
    # Fetch tasks with pagination
    statement = (
        select(Task)
        .where(Task.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    tasks = session.exec(statement).all()
    
    return TasksPublic(data=tasks, count=count)


@router.get("/{task_id}", response_model=TaskPublic)
def read_task(
    task_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Task:
    """
    Get a specific task by ID.
    
    Users can only access their own tasks (unless superuser).
    Requires authentication.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    task_id: uuid.UUID,
    task_in: TaskUpdate,
) -> Task:
    """
    Update a task.
    
    Only the task owner (or superuser) can update it.
    Only updates fields that are provided (partial update).
    Requires authentication.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    task = crud.update_task(session=session, db_task=task, task_update=task_in)
    return task


@router.delete("/{task_id}", response_model=Message)
def delete_task(
    task_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Message:
    """
    Delete a task.
    
    Only the task owner (or superuser) can delete it.
    Requires authentication.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    crud.delete_task(session=session, db_task=task)
    return Message(message="Task deleted successfully")
