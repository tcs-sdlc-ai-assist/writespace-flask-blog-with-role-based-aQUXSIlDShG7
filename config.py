import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-to-a-random-secret-key")
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "local")