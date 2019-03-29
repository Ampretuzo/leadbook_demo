from flask import Flask


def create_app(config="production"):
    app = Flask(__name__)
    if config == "production":
        app.config.from_object("app.configuration.ProductionConfig")
    elif config == "development":
        app.config.from_object("app.configuration.DevelopmentConfig")
    elif config == "testing":
        app.config.from_object("app.configuration.TestingConfig")
    else:
        raise Exception("Invalid configuration")

    return app
