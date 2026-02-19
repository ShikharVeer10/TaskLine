import uuid
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, Task, TaskCreate, TaskUpdate


def create_user(*,session:Session,user_create:UserCreate)->User:
    """Create a new user with hashed password."""
    db_user=User(
        email=user_create.email,
        full_name=user_create.full_name,
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user(*, session: Session, db_user: User, user_update: UserUpdate) -> User:
    """Update a user's details. Handles password hashing if password is changed."""
    user_data = user_update.model_dump(exclude_unset=True)

    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

    db_user.sqlmodel_update(user_data)
    session.commit()
    session.refresh(db_user)
    return db_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """Authenticate a user by email and password."""
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_task(*, session: Session, task_create: TaskCreate, owner_id: uuid.UUID) -> Task:
    """Create a new task. owner_id comes from the authenticated user, not the request body."""
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        status=task_create.status,
        priority=task_create.priority,
        due_date=task_create.due_date,
        owner_id=owner_id,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def update_task(*,session:Session,db_task:Task,task_update:TaskUpdate)->Task:
    task_data=task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(*,session:Session,db_task:Task)->Task:
    session.delete(db_task)
    session.commit()
    return db_task
