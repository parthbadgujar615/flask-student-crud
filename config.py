import os
import secrets

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

    if DATABASE_URL:
        # Railway may provide postgres:// or postgresql://
        # SQLAlchemy needs postgresql+psycopg:// to use psycopg v3
        # Avoid double-replacement if already processed
        if "postgresql+psycopg://" in DATABASE_URL:
            pass  # Already correct
        elif DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL[len("postgres://"):]
        elif DATABASE_URL.startswith("postgresql://"):
            DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL[len("postgresql://"):]

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        "postgresql+psycopg://postgres:1230@localhost/student_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False