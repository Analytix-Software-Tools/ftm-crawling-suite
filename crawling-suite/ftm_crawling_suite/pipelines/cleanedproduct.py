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


class CleanedProductPipeline:
    """This pipeline is responsible for storing the cleaned data inside the data pipeline. In most
    cases, the raw data ref will be stored and processed before a cleaning step is initiated, which
    will then pass in Items of type CleanedProduct to this pipeline step.
    
    The supplier unique ID of the product should be maintained
    in the step preceding this in order to properly identify products throughout every step of the
    cleaning process.
    """
    

    def __init__(self) -> None:
        """Initializes the MongoDB singleton class instance.
        """
        uri_encoded = env['MONGO_URI_PROD_ENCODED'] if env['ENVIRONMENT'] == 'production' else env[
            'MONGO_URI_DEV_ENCODED']
        self.db = MongoClient(uri_encoded)

    def process_item(self, item, spider):
        """Process the item. Check if a document using the same supplier ID and dataRef
        exists.
        """
        item_exists = False
        exists = self.db['crawlingagent']['parsed_products'].find_one(
                {"dataRef": item['dataRef'], "uniqueId": item['uniqueId']})
        if exists is not None:
            item_exists = True
            self.db['crawlingagent']['parsed_products'].replace_one(
                {"dataRef": item['dataRef'], "uniqueId": item['uniqueId']}, item
            )
        if not item_exists:
            self.db['crawlingagent']['parsed_products'].insert_one(dict(item))
        return item
