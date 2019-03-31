import re
import json
import datetime
from datetime import datetime

import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings

from leadbook_crawler.items import (
    SgmaritimeCompanyIndexItem,
    SgmaritimeCompanyProfileItem,
)
from leadbook_crawler.items import SgmaritimeCompanyProfileItemLoader

settings = get_project_settings()


class SgmaritimeCompanyIndexSpider(scrapy.Spider):
    name = "sgmaritime_company_index"

    start_urls = ["https://www.sgmaritime.com/company-listings?page=1"]

    def _parse_companies_from_page(self, response):
        company_listing_selectors = response.selector.xpath(
            "//div[@id='Contentplaceholder1_C025_Col00']//div[contains(concat(' ', @class, ' '), 'company-listing')]"
        )
        for company_listing_selector in company_listing_selectors:
            company_details_selector = company_listing_selector.xpath(
                "div[contains(concat(' ', @class, ' '), ' company-details ')]"
            )
            url_relative = (
                company_details_selector.xpath("*[1]/a/@href")
                .get(default="url-not-found")
                .strip()
            )
            company_name = (
                company_details_selector.xpath("*[1]/a/text()")
                .get(default="name-not-found")
                .strip()
            )
            yield SgmaritimeCompanyIndexItem(
                company_name=company_name,
                url=response.urljoin(url_relative),
                crawled_on=datetime.utcnow(),
            )

    def _on_last_page(self, response):
        pagination_items = response.selector.xpath("//ul[@class = 'pagination']/li")
        last_pagination_item = pagination_items[-1]
        last_pagination_item_a = last_pagination_item.xpath("a")
        return last_pagination_item_a.attrib.get("href", "") == ""

    def _find_next_page_a(self, response):
        if self._on_last_page(response):
            return None
        pagination_items = response.selector.xpath("//ul[@class = 'pagination']/li")
        return pagination_items[-2].xpath("a")[0]

    def _get_current_page_from_url(self, url):
        page_number_match = re.search("page=(\d+)", url)
        if not page_number_match:
            return 1
        return int(page_number_match.group(1))

    def parse(self, response):
        current_page = self._get_current_page_from_url(response.url)
        self.logger.info("Parsing page #%i", current_page)
        for _ in self._parse_companies_from_page(response):
            yield _
        next_page_a = self._find_next_page_a(response)
        if next_page_a is None:
            return
        yield response.follow(next_page_a, callback=self.parse)


class SgmaritimeCompanyProfileSpider(scrapy.Spider):
    """To parse company profies I'm using Splash. I absolutely didn't *need* it, but I figured
    it would be nice to show the integration"""

    name = "sgmaritime_company_profiles"

    def __init__(self, companies_index_jl_path="", *args, **kwargs):
        super(SgmaritimeCompanyProfileSpider, self).__init__(*args, **kwargs)
        assert companies_index_jl_path
        self.companies_index_jl_path = companies_index_jl_path
        script_path = settings.get("SGMARITIME_COMPANY_LUA_PATH", "")
        assert script_path
        self.splash_lua_source = open(script_path, "r").read()

    def start_requests(self):
        with open(self.companies_index_jl_path, "r") as companies_index_file:
            for company_entry_json_str in companies_index_file:
                if not company_entry_json_str or company_entry_json_str.isspace():
                    continue
                company_entry = json.loads(company_entry_json_str)
                # company_name = company_entry['company_name']
                url = company_entry["url"]
                # crawled_on = datetime.strptime(company_entry['crawled_on'], '%Y-%m-%d %H:%M:%S')
                yield SplashRequest(
                    url,
                    self.parse_company,
                    endpoint="execute",
                    args={"lua_source": self.splash_lua_source},
                )

    def _company_page_full(self, response):
        return (
            response.selector.xpath(
                "//div[contains(concat(' ', @class, ' '), ' company-details ')]/h3"
            ).get()
            is not None
        )

    def parse_company(self, response):
        item = None
        loader = SgmaritimeCompanyProfileItemLoader(
            item=SgmaritimeCompanyProfileItem(), response=response
        )
        # Below three values are placed in html in a very volatile way - I prefer to separate them:
        if self._company_page_full(response):
            loader.add_xpath(
                "company_name",
                "//div[contains(concat(' ', @class, ' '), ' company-details ')]/h3/text()",
            )
        else:
            loader.add_xpath(
                "company_name",
                "//div[contains(concat(' ', @class, ' '), ' company-details ')]/text()",
            )
        loader.add_xpath(
            "company_street_address",
            "//div[contains(concat(' ', @class, ' '), ' company-contact ')]/p[1]/text()",
        )
        loader.add_xpath(
            "country",
            "//div[contains(concat(' ', @class, ' '), ' company-contact ')]/p[1]/text()",
        )
        loader.add_value("company_url", response.url)
        loader.add_xpath(
            "company_description",
            "//div[contains(concat(' ', @class, ' '), ' company-profile ')][.//h2/text() = 'Description']//div[contains(concat(' ', @class, ' '), ' company-description ')]/text()",
        )
        loader.add_xpath(
            "category",
            "//div[contains(concat(' ', @class, ' '), ' company-profile ')][.//h2/text() = 'Categories']//li/a[2]/text()",
        )
        loader.add_xpath("company_phone_number", "//div[@id='valuephone']/a/@href")
        loader.add_xpath("company_website", "//div[@id='valuewebsite']/a/@href")
        """NOTE: again, I absolutely didn't need Splash to parse this - company email was out in the open.
        I just used Splash to showcase how to parse SPA/Ajax websites.
        """
        loader.add_xpath("company_email", "//*[@id='companyEmail']/text()")
        loader.add_xpath(
            "business",
            "//div[contains(concat(' ', @class, ' '), ' company-profile ')][.//h2/text() = 'Categories']//li/a[1]/text()",
        )
        loader.add_xpath(
            "contacts",
            "//div[contains(concat(' ', @class, ' '), ' company-contact ')]//p[2]",
        )

        item = loader.load_item()
        yield item
