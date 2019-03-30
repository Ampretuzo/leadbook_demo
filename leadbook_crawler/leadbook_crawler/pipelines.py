# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# # TODO: create celery app and call task queue
# app.send_task('updater.save_company', ({'company_name': 'TEST'},) )

from scrapy.utils.project import get_project_settings
from celery import Celery

from .items import SgmaritimeCompanyProfileItem

settings = get_project_settings()
celery = Celery("updater", broker=settings.get("BROKER_URI"))


class LeadbookCompanyProfileCrawlerPipeline:
    def process_item(self, item, spider):
        if isinstance(item, SgmaritimeCompanyProfileItem):
            celery.send_task("updater.save_company", (dict(item),))
        return item
