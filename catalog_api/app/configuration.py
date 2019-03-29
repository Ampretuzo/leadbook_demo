class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "tmp"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
