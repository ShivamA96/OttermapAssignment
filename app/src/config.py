import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_TOKEN_EXPIRY_MINUTES = int(os.getenv("JWT_TOKEN_EXPIRY_MINUTES", "30"))

DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_FILE = os.getenv("DB_FILE", "database.db")
DB_ECHO = os.getenv("DB_ECHO", "True").lower() in ("true", "1", "t")
DB_URL = f"{DB_TYPE}:///{DB_FILE}" if DB_TYPE == "sqlite" else os.getenv(
    "DB_URL")
DB_CONNECT_ARGS = {"check_same_thread": False} if DB_TYPE == "sqlite" else {}

API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

# Test Data
TEST_USER_NAME = os.getenv("TEST_USER_NAME", "Test Vendor")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "securepassword123")
