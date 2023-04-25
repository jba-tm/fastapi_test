import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_url():
    return "sqlite:///sqlite.db"
    load_dotenv()
    user = os.getenv("DATABASE_USER", "change_this")
    password = os.getenv("DATABASE_PASSWORD", 'change_this')
    server = os.getenv("DATABASE_HOST", '127.0.0.1')
    db = os.getenv("DATABASE_NAME", 'change_this')
    port = os.getenv("DATABASE_PORT", '3306')
    return f"mysql+mysqlconnector://{user}:{password}@{server}:{port}/{db}"


engine = create_engine(get_url(), pool_pre_ping=True, echo=False)

SessionLocal = sessionmaker(
    expire_on_commit=True,
    autocommit=False,
    autoflush=False,
    # twophase=True,
    bind=engine
)
