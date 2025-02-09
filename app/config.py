import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
    # POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    # DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    # REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    # REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
    SECRET_KEY = os.getenv("SECRET_KEY", "gfdmhghif38yrf9ew0jkf32")
    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
