import os

class Config:
    SECRET_KEY = os.environ.get("SESSION_SECRET", "clout-dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///clout.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get("SESSION_SECRET", "clout-dev-secret-change-me")
