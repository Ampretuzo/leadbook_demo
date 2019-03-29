class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "tmp"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    MONGO_URI = "mongodb://localhost:27017/leadbook"


class TestingConfig(Config):
    TESTING = True
