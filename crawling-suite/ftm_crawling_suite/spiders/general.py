from ftm_crawling_suite.items import ProductItem
from scrapy.spiders.crawl import CrawlSpider
from pymongo import MongoClient
from scrapy import signals

class GeneralSpider(CrawlSpider):
    """
    A general spider which is designed to offload data into a pre-designated MongoDB database
    collection.
    """

    # Represents the target collection in which data will be offloaded.
    collection = "products"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Attach the MongoDB signal listener, which will route the collection data accordingly.
        """
        spider = super(GeneralSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self, spider):
        self.logger.info('Spider opened: %s' % spider.name)
