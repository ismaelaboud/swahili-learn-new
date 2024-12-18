from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL configuration with multiple fallback options
def get_database_url():
    # Try environment variables in order of preference
    database_urls = [
        os.getenv("DATABASE_URL"),
        os.getenv("TEST_DATABASE_URL"),
        "sqlite:///./swahili_learn.db"
    ]
    
    for url in database_urls:
        if url:
            return url
    
    raise ValueError("No database URL could be found.")

# Get the database URL
DATABASE_URL = get_database_url()

# Determine if we're using SQLite
is_sqlite = DATABASE_URL.startswith("sqlite")

# Create SQLAlchemy engine with appropriate configuration
if is_sqlite:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=3600,
        echo=False  # Set to True for SQL logging during development
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
