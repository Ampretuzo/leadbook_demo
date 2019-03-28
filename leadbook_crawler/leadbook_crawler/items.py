# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, Compose, TakeFirst
from w3lib.html import remove_tags


class SgmaritimeCompanyIndexItem(scrapy.Item):
    company_name = scrapy.Field()
    url = scrapy.Field()
    crawled_on = scrapy.Field()


class SgmaritimeCompanyProfileItem(scrapy.Item):
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_street_address = scrapy.Field()
    country = scrapy.Field()
    company_description = scrapy.Field()
    category = scrapy.Field()
    company_phone_number = scrapy.Field()
    business = scrapy.Field()
    company_website = scrapy.Field()
    company_email = scrapy.Field()
    contacts = scrapy.Field()


def filter_whitespace_input(value):
    if not value or value.isspace():
        return
    return value


def strip_input(value):
    return value.strip()


def first_word(value):
    return value.split(" ")[0]


def unique(self, value):
    return list(set(value))


def filter_show_email(value):
    if value or value.lower() == "show email":
        return None
    return value


def remove_extra_whitespace(value):
    return " ".join(value.split())


class SgmaritimeCompanyProfileItemLoader(scrapy.loader.ItemLoader):
    company_name_in = Compose(
        MapCompose(strip_input, filter_whitespace_input), Join(" - ")
    )
    company_name_out = TakeFirst()
    company_street_address_in = Compose(
        MapCompose(strip_input, filter_whitespace_input), Join(", ")
    )
    company_street_address_out = TakeFirst()
    country_in = Compose(
        MapCompose(strip_input, filter_whitespace_input, first_word), lambda v: v[-1]
    )
    country_out = TakeFirst()
    company_description_in = Compose(
        MapCompose(strip_input, filter_whitespace_input), Join("\n")
    )
    category_in = unique
    business_in = unique
    contacts_in = Compose(
        MapCompose(
            remove_tags, remove_extra_whitespace, strip_input, filter_whitespace_input
        ),
        Join("\n"),
    )
    company_email_in = MapCompose(strip_input, filter_show_email)
