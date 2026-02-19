
from sqlmodel import Session, select, create_engine
from app.models import User
from app.core.config import settings
from sqlalchemy import text

def check_users():
    print(f"Connecting to database: {settings.DATABASE_URL.replace(settings.DB_PASSWORD, '******')}")
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with Session(engine) as session:
            statement = select(User)
            users = session.exec(statement).all()
            
            if not users:
                print("No users found in the database.")
                print("You should create a user first using the /users/signup endpoint.")
            else:
                print(f"Found {len(users)} user(s):")
                for user in users:
                    print(f"- ID: {user.id}")
                    print(f"  Email: {user.email}")
                    print(f"  Is Active: {user.is_active}")
                    print(f"  Is Superuser: {user.is_superuser}")
                    print(f"  Hashed Password (start): {user.hashed_password[:10]}...")
    except Exception as e:
        print(f"Error checking users: {e}")

if __name__ == "__main__":
    check_users()
