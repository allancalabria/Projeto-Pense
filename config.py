import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Config:
    SECRET_KEY = os.getenv("secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
