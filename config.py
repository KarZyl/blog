# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")