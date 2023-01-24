from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from ftm_crawling_suite.items import CleanedProduct
import uuid


class NissanDataCleaningPipeline:
    """This pipeline step will manage the cleaning of raw Nissan USA data into parsed
    product data. In this step, the raw data is parsed down to a format and nomenclature
    as well as respective units of measurement are retained. This data will be sent to
    a queue where it can be automatically cleaned once for each given product type.
    """

    def parse_specifications_from_raw(self, raw_product):
        """Parse the product's general specifications from the raw data.
        """
        cleaned_specs = []
        if 'specifications' in raw_product:
            for i in range(0, len(raw_product['specifications'])):
                if 'specs' in raw_product['specifications'][i]:
                    for j in range(0, len(raw_product['specifications'][i]['specs'])):
                        if 'unit' in raw_product['specifications'][i]['specs'][j]:
                            cleaned_specs.append({
                                "attributeName": raw_product['specifications'][i]['specs'][j]['unit'],
                                "attributeValue": raw_product['specifications'][i]['specs'][j]['value']
                            })
                else:
                    cleaned_specs.append({
                        "attributeName": raw_product['specifications'][i]['unit'],
                        "attributeValue": raw_product['specifications'][i]['value']
                    })
        return cleaned_specs

    def parse_consumption_specs_from_raw(self, raw_product):
        """Parses vehicle consumption specs from the raw specification list. Generally,
        these are listed as ranges however the ranges reference the same value.
        """
        cleaned_specs = []
        if 'consumptionSpecs' in raw_product:
            for i in range(0, len(raw_product['consumptionSpecs'])):
                if 'specs' in raw_product['consumptionSpecs'][i]:
                    for j in range(0, len(raw_product['consumptionSpecs'][i]['specs'])):
                        if 'unit' in raw_product['consumptionSpecs'][i]['specs'][j]:
                            cleaned_specs.append({
                                "attributeName": raw_product['consumptionSpecs'][i]['specs'][j]['unit'],
                                "attributeValue": {
                                    "minValue": raw_product['consumptionSpecs'][i]['specs'][j]['minValue'],
                                    "maxValue": raw_product['consumptionSpecs'][i]['specs'][j]['maxValue']
                                }
                            })
                else:
                    cleaned_specs.append({
                        "attributeName": raw_product['consumptionSpecs'][i]['unit'],
                        "attributeValue": {
                            "minValue": raw_product['consumptionSpecs'][i]['minValue'],
                            "maxValue": raw_product['consumptionSpecs'][i]['maxValue']
                        }
                    })
        return cleaned_specs

    def parse_accessories_specs_from_raw(self, raw_product):
        """Parses an attribute value from the raw specification based on the structure
        of the data. Returns the data type and the value of the attribute from the spec.

        If the spec contains an array of specs, then parse them out. Otherwise, append the
        spec to the resultant list.
        """
        new_specs = []
        if 'accessoriesSpecs' in raw_product:
            for i in range(0, len(raw_product['accessoriesSpecs'])):
                if 'specs' in raw_product['accessoriesSpecs'][i]:
                    for j in range(0, len(raw_product['accessoriesSpecs'][i]['specs'])):
                        if 'unit' in raw_product['accessoriesSpecs'][i]['specs'][j]:
                            new_specs.append({
                                "attributeName": raw_product['accessoriesSpecs'][i]['specs'][j]['unit'],
                                "attributeValue": raw_product['accessoriesSpecs'][i]['specs'][j]['value'],
                                "type": ""
                            })
                else:
                    new_specs.append({
                        "attributeName": raw_product['accessoriesSpecs']['value'],
                        "attributeValue": "",
                        "type": ""
                    })
        return new_specs

    def process_item(self, item, spider):
        """For each item, parse the product type attributes from 'accessoriesSpecs',
        'consumptionSpecs', and 'specifications'.
        """
        new_specs = []
        raw_product = item['raw']
        new_specs += self.parse_accessories_specs_from_raw(raw_product=raw_product)
        new_specs += self.parse_consumption_specs_from_raw(raw_product=raw_product)
        new_specs += self.parse_specifications_from_raw(raw_product=raw_product)
        parsed_product = CleanedProduct()
        parsed_product['categoryNames'] = raw_product['categoryNames']
        parsed_product['supplierName'] = raw_product['categoryNames'][-1].title() + ' ' + raw_product['trim']
        parsed_product['uniqueId'] = item['uniqueId']
        parsed_product['attributeValues'] = new_specs
        parsed_product['description'] = ""
        parsed_product['pid'] = uuid.uuid4()
        parsed_product['dataRef'] = item['dataRef']
        return parsed_product
