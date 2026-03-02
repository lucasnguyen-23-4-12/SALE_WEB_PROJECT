from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Tạo engine kết nối PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # True để log SQL (dev mode)
)

# Tạo session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class cho ORM models
Base = declarative_base()