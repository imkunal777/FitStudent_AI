"""
config.py – Flask and SQLAlchemy configuration.
All sensitive values are read from environment variables (via .env).
"""
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load variables from .env file if it exists
load_dotenv()


class Config:
    # Flask secret key for session signing and flash messages
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # -------------------------------------------------------
    # MySQL connection via PyMySQL driver
    # URL-encode the password so special chars (@, #, !, etc.) are safe
    # -------------------------------------------------------
    MYSQL_HOST     = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER     = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB       = os.environ.get("MYSQL_DB", "fitstudent_ai")
    MYSQL_PORT     = int(os.environ.get("MYSQL_PORT", 3306))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
