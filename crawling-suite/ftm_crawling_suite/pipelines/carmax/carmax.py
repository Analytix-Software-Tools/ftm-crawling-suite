from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from ftm_crawling_suite.items import CleanedProduct
import uuid


class CarMaxCleaningPipeline:
    """

    Cleaning pipeline for CarsDotCom data.

    """

    def __init__(self):
        """
        Initializes the pipeline with a mapping of attribute field names to the potential options.
        """
        self.attribute_name_to_options = {
            "transmission": {
                "formalName": "Transmission Type",
            },
            "drivetrain": {
                "formalName": "Drivetrain",
            },
            "engineType": {
                "formalName": "Motor Fuel Type",
            }
        }

    def clean_specs(self, raw_product):
        """
        Adds the specifications to the product.
        """
        new_specs = [
            {
                "attributeName": "Model Year",
                "value": {
                    "numValue": raw_product['year']
                }
            },
            {
                "attributeName": "MPG City",
                "value": {
                    "minValue": raw_product['mpgCity'],
                    "maxValue": raw_product['mpgCity']
                }
            },
            {
                "attributeName": "MPG Highway",
                "value": {
                    "minValue": raw_product['mpgHighway'],
                    "maxValue": raw_product['mpgHighway']
                }
            },
            {
                "attributeName": "Number of Cylinders",
                "value": {
                    "numValue": raw_product['cylinders'],
                }
            },
            {
                "attributeName": "Horsepower",
                "value": {
                    "numValue": raw_product['horsepower'],
                }
            },
            {
                "attributeName": "Horsepower (RPM)",
                "value": {
                    "numValue": raw_product['horsepowerRpm'],
                }
            },
            {
                "attributeName": "Engine Size (L)",
                "value": {
                    "numValue": raw_product['engineSize'],
                }
            },
            {
                "attributeName": "Engine Torque",
                "value": {
                    "numValue": raw_product['engineTorque'],
                }
            },
            {
                "attributeName": "Engine Torque (RPM)",
                "value": {
                    "numValue": raw_product['horsepower'],
                }
            },
        ]

        for string_attr in self.attribute_name_to_options:
            new_specs.append({
                "attributeName": self.attribute_name_to_options[string_attr]['formalName'],
                "value": {
                    "options": [],
                    "value": raw_product[string_attr]
                }
            })

        return new_specs

    def process_item(self, item, spider):
        """
        Processes an item in the pipeline. Parses specs from raw.detail.callSourceDniMetadata.dimensions
        """
        raw_product = item['raw']
        parsed_product = CleanedProduct()
        parsed_product['categoryNames'] = raw_product['categoryNames']
        parsed_product['supplierName'] = f"{raw_product['model']} {raw_product['body']} {raw_product['trim']}"
        parsed_product['uniqueId'] = item['uniqueId']
        parsed_product['attributeValues'] = self.clean_specs(raw_product)
        parsed_product['description'] = ""
        parsed_product['pid'] = uuid.uuid4()
        parsed_product['dataRef'] = item['dataRef']
        return parsed_product
