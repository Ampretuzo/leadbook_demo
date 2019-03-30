import os
import string

DB_ADDRESS = os.environ.get("LEADBOOK_MONGO_ADDRESS")
DB_NAME = os.environ.get("LEADBOOK_MONGO_DB")


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "tmp"
    MONGO_URI = string.Template("mongodb://$db_address/$db_name").substitute(
        db_address=DB_ADDRESS, db_name=DB_NAME
    )


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
