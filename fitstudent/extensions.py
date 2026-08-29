"""
extensions.py – Shared Flask extensions instantiated here to avoid circular imports.
Import `db` from this module in models and app.py.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
