import logging

from celery import Celery

# from celery.contrib import rdb
from pymongo import MongoClient

from config import db_uri, broker_uri, DB_NAME

# Retry in 5 minutes
RETRY_DELAY_SEC = 60 * 5


app = Celery("updater", broker=broker_uri)


@app.task(bind=True)
def save_company(self, document):
    company_name = document["company_name"]
    try:
        with MongoClient(db_uri) as connection:
            db = connection[DB_NAME]
            result = db.sgmaritime.replace_one(
                {"company_name": company_name}, document, upsert=True
            )
            if result.matched_count:
                logging.info("Updated %s", company_name)
            else:
                logging.info("Saved %s", company_name)
    except Exception as exception:
        logging.warn("Could not process %s", company_name)
        self.retry(countdown=RETRY_DELAY_SEC, exc=exception, max_retries=1)
