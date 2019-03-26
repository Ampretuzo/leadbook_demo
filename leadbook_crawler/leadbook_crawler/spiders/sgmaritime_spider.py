import re

import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response


class SgmaritimeCompaniesSpider(scrapy.Spider):
    name = "sgmaritime_companies"

    start_urls = ["https://www.sgmaritime.com/company-listings?page=329"]

    def _parse_companies_from_page(self, response):
        return
        # TODO: enable company parsing
        companies_link_extractor = LinkExtractor(allow=r"/companies/.+")
        for company_link in companies_link_extractor.extract_links(response):
            yield SplashRequest(
                company_link.url,
                self.parse_company,
                endpoint="render.html",
                args={
                    # TODO
                },
            )
            return

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

    def parse(self, response):
        current_page = int(re.search("page=(\d+)", response.url).group(1))
        self.logger.info("Parsing page #%i", current_page)
        self._parse_companies_from_page(response)
        next_page_a = self._find_next_page_a(response)
        if next_page_a is None:
            return
        yield response.follow(next_page_a, callback=self.parse)

    def parse_company(self, response):
        # company_name = response.selector.xpath("//div[contains(concat(' ', @class, ' '), ' company-details ')][1]/h3[1]/text()").get()
        pass
