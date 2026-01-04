from sqlmodel import create_engine, Session
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variables
# Use SQLite for local development if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with SQLite-specific settings
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session() -> Generator[Session, None, None]:
    """Generator for database sessions."""
    with Session(engine) as session:
        yield session