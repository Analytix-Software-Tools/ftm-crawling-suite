# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from ftm_crawling_suite.db.db import MongoDBSingleton


class CleanedProductPipeline:
    """This pipeline is responsible for storing the cleaned data inside the data pipeline. In most
    cases, the raw data ref will be stored and processed before a cleaning step is initiated, which
    will then pass in Items of type CleanedProduct to this pipeline step.
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
