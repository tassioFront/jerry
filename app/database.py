"""Database connection and session management"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.config import settings
from app.models.Base import Base


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables (creates all tables)"""
    Base.metadata.create_all(bind=engine)


# def create_test_engine(database_url: str):
#     """
#     Create a test database engine with different configuration.
    
#     Args:
#         database_url: Test database URL
        
#     Returns:
#         SQLAlchemy engine configured for testing
#     """
#     return create_engine(
#         database_url,
#         poolclass=StaticPool,
#         connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
#         echo=False
#     )

