# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem


class GifDownloadPipeline(FilesPipeline):
    def process_item(self, item, spider):
        print item
        if len(item['files']):
            return item


class DoutulaScraperPipeline(object):
    def __init__(self, uri, port, db, collections, file_path):
        self.mongo_uri = uri
        self.mongo_port = port
        self.mongo_db = db
        self.file_path = file_path
        self.img_col = collections[0]
        self.tag_col = collections[1]
        self.rel_col = collections[2]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
			uri = crawler.settings.get("MONGO_URI"),
			port = crawler.settings.get("MONGO_PORT"),
            db = crawler.settings.get("MONGO_DB"),
            collections = [
                crawler.settings.get("IMAGES_COLLECTION"),
                crawler.settings.get("TAGS_COLLECTION"),
                crawler.settings.get("RELATION_COLLECTION")
                ],
            file_path = crawler.settings.get("FILES_STORE")
            )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port)
            self.db = self.client[self.mongo_db]
        except pymongo.errors as e:
            logging.error(e)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if len(item['files']) == 0:
            logging.info("##########################################")
            logging.info("IMG: {} not able to download!i\nURL: {}".format(item['title'], item['url']))
            logging.info("##########################################")
            return 

        image = {}
        image['_id'] = item['_id']
        image['url'] = item['url']
        image['image_url'] = item['file_urls'][0]
        image['path'] = self.file_path + '/' + item['files'][0]['path']
        image['title'] = item['title']

        self.db[self.img_col].insert(image)

        for tag in item['tags']:
            tag_obj = self.db[self.tag_col].find_one({'name': tag})
            if tag_obj:
                self.db[self.rel_col].insert({
                    'tag_id': tag_obj['_id'],
                    'image_id': image['_id']
                    })
            else:
                tag_id = self.db[self.tag_col].insert({
                    'name': tag
                    })
                self.db[self.rel_col].insert({
                    'tag_id': tag_id,
                    'image_id': image['_id']
                    })
