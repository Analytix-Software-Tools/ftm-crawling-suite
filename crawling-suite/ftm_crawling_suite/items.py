# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.exceptions import DropItem


class RawItem(scrapy.Item):
    """Represents a raw item to be stored
    within the database. This is mainly to unify the tagged raw data.
    """

    # Represents the source of the data item.
    dataRef = scrapy.Field()

    # Represents the collection that this data item corresponds
    # to.
    collection = scrapy.Field()

    # Represents the raw data being stored.
    raw = scrapy.Field()

    # Assign a unique identifier to retrieve this entry in the future.
    uniqueId = scrapy.Field()


class DataReferenceTag(scrapy.Item):
    """
    Stores general information regarding a crawled item, such as the
    reference of where it was obtained.
    """

    # The reference ID of the item indicating which source crawler the item
    # originated from.
    dataRef = scrapy.Field()

    # The hostname the item was crawled from.
    host = scrapy.Field()

    # The datetime the item was updated or added.
    last_updated = scrapy.Field()

    # Unique identifier.
    pid = scrapy.Field()


class ProductItem(DataReferenceTag):
    """
    Parsed products have been parsed and accepted thru the in-app validation section. They
    are presumably ready to be pushed to the database, however they must be associated with
    the correct organization.
    """

    # The organization the product belongs to.
    organizationName = scrapy.Field()

    # The name of the item.
    name = scrapy.Field()

    # A unique ID provided by the supplier.
    supplierId = scrapy.Field()

    # Attribute values of the product which take the form "attributeName" and "attributeValue"
    # as well as "attributePid".
    attributeValues = scrapy.Field()

    # The image URL.
    imgUrl = scrapy.Field()

    # Description of the item.
    description = scrapy.Field()

    # Array of potential product categories. Will need to feed this into a
    # classification model.
    productCategories = scrapy.Field()

    # The source URL of the product details.
    sourceUrl = scrapy.Field()

    def validate(self):
        """
        Validates the ProductItem fields.
        """
        if self.name is None or not isinstance(self.name, str):
            raise DropItem("Name must be a string!")
        elif self.description is None or not isinstance(self.description, str):
            raise DropItem("Description must be a string!")
        elif self.productCategories is None or not isinstance(self.productCategories, list):
            raise DropItem("Field 'productCategories' must be a list!")
        elif self.attributeValues is None or not isinstance(self.attributeValues, list):
            raise DropItem("Field 'attributeValues' must be a list!")
        elif self.supplierId is None or not isinstance(self.supplierId, str):
            raise DropItem("Field 'supplierId' must be a string!")

        for attr_val in self.attributeValues:
            if 'attributeName' not in attr_val or 'attributeValue' not in attr_val:
                raise DropItem(f"Attribute value ")


class CleanedProduct(scrapy.Item):
    """After being stored as a raw data ref, a product will undergo a transformation
    to be cleaned and processed to the taxonomy used within the application. This is
    the step in which all raw names and values are retained before the nomenclature
    and respective values of the data are transformed.

    """

    # Represents the source identifier for the data.
    dataRef = scrapy.Field()

    # Represents the name of the product.
    supplierName = scrapy.Field()

    # A unique, short paragraph or sentence explaining the product.
    description = scrapy.Field()

    # Represents the attribute values tied to the product with the name, the data
    # type, and the value.
    attributeValues = scrapy.Field()

    # Represents a list of hierarchical category names for the product.
    categoryNames = scrapy.Field()

    # A unique identifier for the raw product.
    pid = scrapy.Field()

    # A field to store the original ID from the supplier.
    uniqueId = scrapy.Field()


class OrganizationHtml(DataReferenceTag):
    """
    Structure representing website text crawled from an organization website
    URL, tagged by domain.
    """
    string = scrapy.Field()
    domain = scrapy.Field()
    sourceUrl = scrapy.Field()
    index = scrapy.Field()
