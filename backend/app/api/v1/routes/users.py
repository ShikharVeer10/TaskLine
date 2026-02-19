"""
User management endpoints.

POST /users/signup     →  Register a new user
GET  /users/me         →  Get current user's profile
PATCH /users/me        →  Update current user's profile
GET  /users/{user_id}  →  Get a user by ID (superuser only)
"""
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, func

from app import crud
from app.api.deps import SessionDep, CurrentUser
from app.models import (
    User,
    UserCreate,
    UserPublic,
    UsersPublic,
    UserUpdate,
    Message,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: UserCreate) -> User:
    """
    Register a new user account.
    
    This endpoint is public — no authentication required.
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )
    
    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> User:
    """
    Get the current logged-in user's profile.
    
    Requires authentication (Bearer token).
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, current_user: CurrentUser, user_in: UserUpdate
) -> User:
    """
    Update the current user's profile.
    
    Only updates fields that are provided (partial update).
    Requires authentication.
    """
    # If changing email, check it's not already taken
    if user_in.email:
        existing_user = session.exec(
            select(User).where(User.email == user_in.email)
        ).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )

    user = crud.update_user(session=session, db_user=current_user, user_update=user_in)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: str, session: SessionDep, current_user: CurrentUser
) -> User:
    """
    Get a specific user by ID.
    
    - Regular users can only read their own profile.
    - Superusers can read any user's profile.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not current_user.is_superuser and user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user
