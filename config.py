import os


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://timi:goodness@localhost/library_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = os.urandom(16)
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    RATELIMIT_HEADERS_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    # Use an in-memory database
    SQLALCHEMY_DATABASE_URI = "sqlite://"
