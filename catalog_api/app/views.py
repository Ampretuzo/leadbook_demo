from flask import request


from app.serializers import company_schema, companies_schema


def companies_endpoint():
    company_search_string = request.args.get("company_name")
    return companies_schema.jsonify([{"company_name": "1"}, {"company_name": "2"}])


def company_endpoint(company_name):
    return company_schema.jsonify({"company_name": "A Company"})
