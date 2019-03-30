import logging

from celery import Celery

# from celery.contrib import rdb
from pymongo import MongoClient

from config import db_uri, broker_uri, DB_NAME


app = Celery("updater", broker=broker_uri)


@app.task
def save_company(document):
    company_name = document["company_name"]
    with MongoClient(db_uri) as connection:
        db = connection[DB_NAME]
        result = db.sgmaritime.replace_one(
            {"company_name": company_name}, document, upsert=True
        )
        if result.matched_count:
            logging.info("Updated %s", company_name)
        else:
            logging.info("Saved %s", company_name)
