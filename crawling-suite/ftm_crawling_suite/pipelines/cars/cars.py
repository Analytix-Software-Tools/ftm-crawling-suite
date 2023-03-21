from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from ftm_crawling_suite.items import CleanedProduct
import uuid


class CarsDotComCleaningPipeline:
    """
    
    Cleaning pipeline for CarsDotCom data.

    """

    def process_dimensions(self, raw_product):
        """
        Processes the dimensions for the given product.
        """
        pass

    def process_item(self, item, spider):
        """
        Processes an item in the pipeline. Parses specs from raw.detail.callSourceDniMetadata.dimensions
        """
        new_specs = []
        raw_product = item['raw']
        parsed_product = CleanedProduct()
        parsed_product['categoryNames'] = raw_product['categoryNames']
        parsed_product['supplierName'] = raw_product['categoryNames'][-1].title() + ' ' + raw_product['trim']
        parsed_product['uniqueId'] = item['uniqueId']
        parsed_product['attributeValues'] = new_specs
        parsed_product['description'] = ""
        parsed_product['pid'] = uuid.uuid4()
        parsed_product['dataRef'] = item['dataRef']
        return parsed_product
