from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

connect_args = {}
if settings.DB_ENGINE == "sqlite":
    connect_args["check_same_thread"] = False
elif settings.DB_ENGINE == "postgresql":
    connect_args["sslmode"] = "require"

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
