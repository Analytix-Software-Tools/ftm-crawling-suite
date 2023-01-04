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
