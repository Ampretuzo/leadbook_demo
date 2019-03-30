from flask_marshmallow import Marshmallow

from app import ma


class CompanySchema(ma.Schema):
    company_name = ma.Str()
    company_url = ma.Str()
    company_street_address = ma.Str()
    country = ma.Str()
    company_description = ma.Str()
    categories = ma.List(ma.Str(), attribute="category")
    businesses = ma.List(ma.Str(), attribute="business")
    company_phone_number = ma.Str()
    company_website = ma.Str()
    company_email = ma.Str()
    contacts = ma.List(ma.Str())


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
