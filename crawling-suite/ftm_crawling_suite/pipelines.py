# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import os
from datetime import datetime
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.exceptions import DropItem
import base64
import pymongo
import os


class MongoDBSingleton:
    """
    Singleton class which persists the MongoClient connection throughout the lifecycle
    of the application.
    """
    __instance = None

    @staticmethod
    def get_instance():
        if MongoDBSingleton.__instance is None:
            MongoDBSingleton()
        return MongoDBSingleton.__instance

    def __init__(self):
        if MongoDBSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            mongo_uri_encoded = os.environ.get('MONGO_URI_PROD_ENCODED', 'bW9uZ29kYjovL2xvY2FsaG9zdDoyNzAxOQ==')
            mongo_uri = base64.b64decode(mongo_uri_encoded).decode('utf-8')
            MongoDBSingleton.__instance = pymongo.MongoClient(mongo_uri)


class MongoPipeline:
    """The default pipeline. This item pipeline is responsible for tagging and storing the
    parsed data into the raw_data Mongo collection.
    """

    def __init__(self, db, mongo_collection) -> None:
        """
        Initialize a new MongoPipeline instance.
        """
        self.db = db
        self.collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        """
        Creates a new pipeline instance from the crawler which invokes the pipeline.
        """
        collection_name = crawler.settings.get("collection")
        if collection_name is None:
            raise Exception(f"Crawler {crawler.__class__} requires field 'collection' to be defined!")
        try:
            analytix_db = MongoDBSingleton.get_instance()
            return cls(
                db=analytix_db,
                mongo_collection=collection_name
            )
        except pymongo.errors.ConnectionFailure:
            # TODO: Implement proper error handling.
            print("Database connection failed.")

    def process_item(self, item, spider):
        """Process the item. Check if a document using the same supplier ID and dataRef
        exists.
        """
        item_exists = False
        exists = self.db['crawlingagent'][self.collection].find_one(
            {"dataRef": item['dataRef'], "uniqueId": item['uniqueId']})
        if exists is not None:
            item_exists = True
            self.db['crawlingagent'][self.collection].replace_one(
                {"dataRef": item['dataRef'], "uniqueId": item['uniqueId']}, item
            )
        if not item_exists:
            self.db['crawlingagent'][self.collection].insert_one(dict(item))
        yield item


class DataTagPipeline:
    """
    Attach general tags to the data to uniquely separate it and make it
    traceable.
    """

    def process_item(self, item, spider):
        item['host'] = os.uname()[1]
        item['last_updated'] = datetime.now()
        item['dataReferenceId'] = spider.name
        yield item


from scrapy.exceptions import DropItem


class ValidateProductFields:
    """
    Validates product fields to ensure certain required fields are present.
    """

    def process_item(self, item, spider):
        """
        Ensure all fields are present in an item.
        """
        for field in item:
            if field is None:
                raise DropItem(f"Error: field {field} cannot be None.")
            elif field == 'attributeValues' and not isinstance(field, list) or len(field) == 0:
                raise DropItem(f"Field 'attributeValues' must be a list of length >= 1! Dropping item...")
            if field == 'attributeValues':
                for attribute_value in field:
                    if not attribute_value['attributePid'] or not attribute_value['attributeValue']:
                        raise DropItem(f"Invalid attributeValue! Dropping item.")
