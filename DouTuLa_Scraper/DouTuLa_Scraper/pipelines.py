# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from DouTuLa_Scraper.config import MongoConfig
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem


class ImagesDownloadPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return item


class DoutulaScraperPipeline(object):
    def __init__(self, uri, port, db, collection):
        self.mongo_uri = uri
        self.mongo_port = port
        self.mongo_db = db
        self.mongo_col = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
			uri = crawler.settings.get("MONGO_URI"),
			port = crawler.setting.get("MONGO_PORT"),
            db = crawler.setting.get("MONGO_DB"),
            colllection = crawler.setting.get("MONGO_COLLECTION")
            )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port)
            self.db = self.client[self.mongo_db][self.mongo_col]
        except pymongo.errors as e:
            logging.error(e)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print item
        pass
