
from sqlmodel import Session, select, create_engine
from app.models import User, UserCreate
from app.core.config import settings
from app.crud import create_user
from app.core.security import get_password_hash

def create_admin():
    print(f"Connecting to database...")
    engine = create_engine(settings.DATABASE_URL)
    
    email = settings.FIRST_SUPERUSER_EMAIL
    password = settings.FIRST_SUPERUSER_PASSWORD
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            print(f"User {email} already exists.")
            # Optional: Reset password if you want to be sure
            # user.hashed_password = get_password_hash(password)
            # session.add(user)
            # session.commit()
            # print(f"Password reset to '{password}'")
        else:
            print(f"Creating user {email}...")
            user_in = UserCreate(
                email=email,
                password=password,
                full_name="Admin User",
                is_superuser=True,
                is_active=True
            )
            create_user(session=session, user_create=user_in)
            print(f"User created successfully.")
            print(f"Email: {email}")
            print(f"Password: {password}")

if __name__ == "__main__":
    create_admin()
