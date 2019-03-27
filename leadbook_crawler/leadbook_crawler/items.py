# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SgmaritimeCompanyIndexItem(scrapy.Item):
    company_name = scrapy.Field()
    url = scrapy.Field()
    crawled_on = scrapy.Field()


class SgmaritimeCompanyProfileItem(scrapy.Item):
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_streetaddress = scrapy.Field()
    country = scrapy.Field()
    company_description = scrapy.Field()
    category = scrapy.Field()
    company_phone_number = scrapy.Field()
    business = scrapy.Field()
    company_website = scrapy.Field()
    company_email = scrapy.Field()
    contacts = scrapy.Field()
