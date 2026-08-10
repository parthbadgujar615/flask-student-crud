import os
import sys
import secrets

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    # Railway may use different variable names depending on the Postgres plugin version
    DATABASE_URL = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("DATABASE_PRIVATE_URL")
        or os.environ.get("DATABASE_PUBLIC_URL")
        or os.environ.get("POSTGRES_URL")
        or ""
    ).strip()

    if DATABASE_URL:
        # Railway provides postgres:// or postgresql://
        # SQLAlchemy needs postgresql+psycopg:// to use psycopg v3
        if "postgresql+psycopg://" in DATABASE_URL:
            pass  # Already correct
        elif DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL[len("postgres://"):]
        elif DATABASE_URL.startswith("postgresql://"):
            DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL[len("postgresql://"):]

        # Log the host (mask password) so we can verify the connection target
        try:
            at_idx = DATABASE_URL.index("@")
            print(f"[CONFIG] Connecting to: ...{DATABASE_URL[at_idx:]}", file=sys.stderr)
        except ValueError:
            print(f"[CONFIG] DATABASE_URL is set but has unexpected format", file=sys.stderr)
    else:
        print("[CONFIG] WARNING: No DATABASE_URL found in environment!", file=sys.stderr)
        print(f"[CONFIG] Available env vars: {[k for k in os.environ if 'PG' in k or 'DATABASE' in k or 'POSTGRES' in k]}", file=sys.stderr)

    # In production (Railway), fail fast if no database URL is provided
    # instead of silently connecting to localhost
    if not DATABASE_URL and os.environ.get("RAILWAY_ENVIRONMENT"):
        raise RuntimeError(
            "DATABASE_URL is not set! Add a PostgreSQL database to your Railway project "
            "and link the DATABASE_URL variable to your web service."
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        "postgresql+psycopg://postgres:1230@localhost/student_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False