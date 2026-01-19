"""
Database module for handling SQLModel database connections and engine setup.
"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator, AsyncGenerator
from contextlib import contextmanager, asynccontextmanager
from .config import settings

import urllib.parse

# Determine if we're using SQLite or PostgreSQL to set appropriate connection parameters
parsed_url = urllib.parse.urlparse(settings.database_url)
is_sqlite = parsed_url.scheme.lower() == 'sqlite'

if is_sqlite:
    # SQLite doesn't support connection pooling or many other parameters
    engine = create_engine(
        settings.database_url,
        echo=settings.db_echo
    )
else:
    # Create the database engine with proper connection pooling for Neon Serverless PostgreSQL
    engine = create_engine(
        settings.database_url,
        echo=settings.db_echo,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_timeout=settings.db_pool_timeout,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=settings.db_pool_recycle,  # Recycle connections
        connect_args={
            "connect_timeout": 10,
        }
    )


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    """
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager for getting a database session.
    Handles session lifecycle automatically.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.
    """
    with Session(engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[Session, None]:
    """
    Get an async database session for async dependency injection.
    """
    async with Session(engine) as session:
        yield session