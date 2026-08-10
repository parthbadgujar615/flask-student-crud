import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback-secret-key"

    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        # Railway may provide:
        # postgresql://...
        # or postgres://...
        #
        # Explicitly use Psycopg 3 with SQLAlchemy.
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        ).replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        "postgresql+psycopg://postgres:1230@localhost/student_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False