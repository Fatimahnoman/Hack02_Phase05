from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from ..config import settings
import os

# Ensure the directory for the SQLite file exists
db_path = "todo_app.db"
db_dir = os.path.dirname(db_path)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

# Create the database engine with appropriate options for both SQLite and PostgreSQL
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True for debugging
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url.lower() else {}
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create database tables if they don't exist"""
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise