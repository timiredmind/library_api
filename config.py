import os


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://timi:goodness@localhost/library_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = os.urandom(16)
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
