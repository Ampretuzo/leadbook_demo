import os
import string

DB_ADDRESS = os.environ.get("LEADBOOK_MONGO_ADDRESS")
DB_NAME = os.environ.get("LEADBOOK_MONGO_DB")
RABBIT_ADDRESS = os.environ.get("LEADBOOK_RABBIT_ADDRESS")
RABBIT_UNAME = os.environ.get("LEADBOOK_RABBIT_UNAME")
RABBIT_PWD = os.environ.get("LEADBOOK_RABBIT_PWD")

db_uri = string.Template("mongodb://$db_address/").substitute(db_address=DB_ADDRESS)


broker_uri = string.Template(
    "amqp://$broker_uname:$broker_pwd@$broker_address"
).substitute(
    broker_uname=RABBIT_UNAME, broker_pwd=RABBIT_PWD, broker_address=RABBIT_ADDRESS
)
