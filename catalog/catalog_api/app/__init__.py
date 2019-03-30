from flask import Flask
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo


ma = Marshmallow()
mongo = PyMongo()


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

    ma.init_app(app)
    mongo.init_app(app)

    app.add_url_rule("/companies", "companies", views.companies_endpoint)
    app.add_url_rule(
        "/companies/<string:company_name>", "company", views.company_endpoint
    )

    return app


from app import views
