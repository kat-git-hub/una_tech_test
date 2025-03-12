import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'glucose.db')}"
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
