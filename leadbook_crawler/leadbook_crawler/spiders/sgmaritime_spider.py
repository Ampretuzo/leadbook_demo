import re
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


settings = get_project_settings()


class SgmaritimeCompaniesSpider(scrapy.Spider):
    name = "sgmaritime_companies"

    start_urls = ["https://www.sgmaritime.com/company-listings?page=1"]

    def __init__(self, *args, **kwargs):
        super(SgmaritimeCompaniesSpider, self).__init__(*args, **kwargs)
        script_path = settings.get("SGMARITIME_COMPANY_LUA_PATH", None)
        assert script_path is not None
        self.splash_lua_source = open(script_path, "r").read()

    def _load_company_pages(self, response):
        companies_link_extractor = LinkExtractor(allow=r"/companies/.+")
        for company_link in companies_link_extractor.extract_links(response):
            yield SplashRequest(
                company_link.url,
                self.parse_company,
                endpoint="execute",
                args={"lua_source": self.splash_lua_source},
            )

    def _parse_companies_from_page(self, response):
        listing_container_selector = response.selector.xpath(
            "//div[@id='Contentplaceholder1_C025_Col00'][1]/div[last()]"
        )
        company_listing_selectors = listing_container_selector.xpath(
            "div[@class='row']/div[@class='company-listing']"
        )
        for company_listing_selector in company_listing_selectors:
            company_details_selector = company_listing_selector.xpath(
                "div[contains(concat(' ', @class, ' '), ' company-details ')][1]"
            )
            url_relative = company_details_selector.xpath("*/a/@href").get()
            company_name_raw = company_details_selector.xpath("*/a/text()").get()
            company_name = company_name_raw.strip() if company_name_raw else ""
            yield SgmaritimeCompanyIndexItem(
                company_name=company_name,
                url=response.urljoin(url_relative),
                crawled_on=datetime.utcnow(),
            )
            # yield response.follow(url_relative, callback=self.parse_company)
        for _ in self._load_company_pages(response):
            yield _

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

    def _company_page_full(self, response):
        return (
            response.selector.xpath(
                "//div[contains(concat(' ', @class, ' '), ' company-details ')]/h3"
            ).get()
            is not None
        )

    def parse_company(self, response):
        item = None
        loader = ItemLoader(item=SgmaritimeCompanyProfileItem(), response=response)
        # Below three values are placed in html in a very volatile way - I prefer to separate them:
        if self._company_page_full(response):
            loader.add_xpath(
                "company_name",
                "//div[contains(concat(' ', @class, ' '), ' company-details ')]/h3/text()",
            )
            loader.add_xpath(
                "company_streetaddress",
                "//div[contains(concat(' ', @class, ' '), ' company-contact ')]/p[1]/text()",
            )
            loader.add_xpath(
                "country",
                "//div[contains(concat(' ', @class, ' '), ' company-contact ')]/p[1]/text()",
            )
        else:
            loader.add_xpath(
                "company_name",
                "//div[contains(concat(' ', @class, ' '), ' company-details ')]/text()",
            )
            loader.add_xpath(
                "company_streetaddress",
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
            "//div[contains(concat(' ', @class, ' '), ' company-profile ')][.//h2/text() = 'Categories']//div[contains(concat(' ', @class, ' '), ' company-description ')]//a/text()",
        )
        loader.add_xpath("company_phone_number", "//div[@id='valuephone']/a/@href")
        loader.add_xpath("company_website", "//div[@id='valuewebsite']/a/@href")
        """NOTE: I absolutely didn't need Splash to parse this - company email was out in the open.
        I just used Splash to showcase how to parse SPA/Ajax websites.
        """
        loader.add_xpath(
            "company_email",
            "//*[@id='enquiry-contentblock' and not(contains(@style, 'none'))]//*[@id='companyEmail']/text()",
        )
        # TODO
        # loader.add_xpath('business', "")
        # loader.add_xpath('contacts', "")

        item = loader.load_item()
        yield item
