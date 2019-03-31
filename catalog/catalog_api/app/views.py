import string
import json

from flask import Response, request

from app.serializers import company_schema, companies_schema
from app import mongo


def companies_endpoint():
    company_search_string = request.args.get("company_name")
    search_dict = {}
    if company_search_string:
        search_dict["company_name"] = {
            "$regex": string.Template(".*$search_key.*").substitute(
                search_key=company_search_string
            )
        }
    result_cursor = mongo.db.sgmaritime.find(search_dict)
    return companies_schema.jsonify(list(result_cursor))


def company_endpoint(company_name):
    company = mongo.db.sgmaritime.find_one({"company_name": company_name})
    if company:
        return company_schema.jsonify(company)
    else:
        return Response(
            response=json.dumps({"status": "Company with given name not found"}),
            status=404,
            content_type="application/json",
        )
