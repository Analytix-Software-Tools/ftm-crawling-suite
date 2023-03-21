from scrapy.exceptions import DropItem
from ftm_crawling_suite.db.db import MongoDBSingleton


class FilterDuplicatesPipeline:
    """
    Pipeline used for filtering out any duplicates that exist by filtering out by the unique ID without the
    dataRef tag.
    """

    def __init__(self) -> None:
        """Initializes the MongoDB singleton class instance.
        """
        self.db = MongoDBSingleton.get_instance()

    def process_item(self, item, spider):
        """
        Process items in the pipeline. Check the database to verify whether an item exists such that its
        dataRef does NOT match the item's however the IDs are shared.
        """
        exists = self.db['crawlingagent']['raw_data'].find_one({"uniqueId": item['uniqueId'],
                                                                "dataRef": {"$ne": item['dataRef']}})
        if exists is not None:
            raise DropItem(f"Item exists with ID {item['uniqueId']}.")
        return item
