# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.exceptions import DropItem
import pydotenv

# Initialize the app environment.
env = pydotenv.Environment()

class FtmCrawlingSuitePipeline:
    """The default pipeline. This item pipeline is responsible for tagging and storing the
    parsed data into the raw_data Mongo collection.
    """

    def __init__(self) -> None:
        """Initializes the MongoDB singleton class instance.
        """
        uri_encoded = env['MONGO_URI_PROD_ENCODED'] if env['ENVIRONMENT'] == 'production' else env['MONGO_URI_DEV_ENCODED']
        self.db = MongoClient(uri_encoded)

    def process_item(self, item, spider):
        """Process the item. Check if the a document using the same supplier ID and dataRef
        exists.
        """
        is_data_valid = True
        for data in item:
            if not data:
                is_data_valid = False
                raise DropItem("Missing {0}!".format(data))
            exists = self.db['crawlingagent']['raw_data'].find_one({"dataRef": item['dataRef'], "uniqueId": item['uniqueId']})
            # TODO: Need to update this in case that the listing changes.
            if exists is not None:
                is_data_valid = False
                raise DropItem(f"Item {data} exists! Skipping...")
        if is_data_valid:
            self.db['crawlingagent']['raw_data'].insert_one(dict(item))
        return item
