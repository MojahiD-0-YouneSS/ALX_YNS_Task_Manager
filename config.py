import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///YNS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'mp3', 'mp4'}

