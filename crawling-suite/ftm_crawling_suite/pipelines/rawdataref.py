# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from ftm_crawling_suite.db.db import MongoDBSingleton


class RawDataRefPipeline:
    """The default pipeline. This item pipeline is responsible for tagging and storing the
    parsed data into the raw_data Mongo collection.
    """

    def __init__(self) -> None:
        """Initializes the MongoDB singleton class instance.
        """
        self.db = MongoDBSingleton.get_instance()

    def process_item(self, item, spider):
        """Process the item. Check if a document using the same supplier ID and dataRef
        exists.
        """
        item_exists = False
        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))
        exists = self.db['crawlingagent']['raw_data'].find_one(
                {"dataRef": item['dataRef'], "uniqueId": item['uniqueId']})
        if exists is not None:
            item_exists = True
            self.db['crawlingagent']['raw_data'].replace_one(
                {"dataRef": item['dataRef'], "uniqueId": item['uniqueId']}, item
            )
        if not item_exists:
            self.db['crawlingagent']['raw_data'].insert_one(dict(item))
        return item
