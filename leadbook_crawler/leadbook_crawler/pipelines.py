# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# # TODO: create celery app and call task queue
# app.send_task('updater.save_company', ({'company_name': 'TEST'},) )


class LeadbookCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
