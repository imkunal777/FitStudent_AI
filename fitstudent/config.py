"""
config.py – Flask and SQLAlchemy configuration.
All sensitive values are read from environment variables (via .env).

Database selection (automatic):
  - If MYSQL_HOST env var is set  → uses MySQL via PyMySQL
  - Otherwise                     → uses SQLite (fitstudent.db in project root)
    This makes the app deployable on Streamlit Cloud / any host with no MySQL.
"""
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load variables from .env file if it exists
load_dotenv()


def _build_db_uri() -> str:
    """Return the best available database URI for this environment."""
    mysql_host = os.environ.get("MYSQL_HOST", "").strip()

    if mysql_host:
        # MySQL is configured – use it
        user     = os.environ.get("MYSQL_USER", "root")
        password = quote_plus(os.environ.get("MYSQL_PASSWORD", ""))
        db       = os.environ.get("MYSQL_DB", "fitstudent_ai")
        port     = int(os.environ.get("MYSQL_PORT", 3306))
        return f"mysql+pymysql://{user}:{password}@{mysql_host}:{port}/{db}"

    # Fallback: SQLite – no server required, works on Streamlit Cloud
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path  = os.path.join(base_dir, "fitstudent.db")
    return f"sqlite:///{db_path}"


class Config:
    # Flask secret key for session signing and flash messages
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    SQLALCHEMY_DATABASE_URI    = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

