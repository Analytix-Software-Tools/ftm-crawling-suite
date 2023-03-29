# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RawDataRef(scrapy.Item):
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


class ProductTypeValidation(scrapy.Item):
    """
    Is mapped in-app to provide context and instructions for final cleaning for a given crawled
    product item. These can be used to assist with prediction of new values.
    """
    pid = scrapy.Field()

    supplierProductTypeName = scrapy.Field()

    productTypeAttributeValues = scrapy.Field()


class ParsedProduct(scrapy.Item):
    """
    Parsed products have been parsed and accepted thru the in-app validation section. They
    are presumably ready to be pushed to the database, however they must be associated with
    the correct organization.
    """

    # The organization the product belongs to.
    organizationName = scrapy.Field()

    # The name.
    name = scrapy.Field()

    # Attribute values of the product which take the form "attributeName" and "attributeValue"
    # as well as "attributePid".
    attributeValues = scrapy.Field()

    # The image URL.
    imgUrl = scrapy.Field()

    description = scrapy.Field()

    # The PID of the product type.
    productTypePid = scrapy.Field()

    # The source URL of the product details.
    source = scrapy.Field()


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


class OrganizationUrlMapping:
    """
    A mapping of organization to the URLs of that organization.
    """
    organizationPid = scrapy.Field()

    urls = scrapy.Field()

    startUrl = scrapy.Field()

    lastCrawledDate = scrapy.Field()
