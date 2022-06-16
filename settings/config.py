import os

from dotenv import load_dotenv

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_KEY", "super_secret_key")
ALGORITHM = "HS256"

DATABASE_HOST = os.getenv("DATABASE_HOST", "database")
DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
