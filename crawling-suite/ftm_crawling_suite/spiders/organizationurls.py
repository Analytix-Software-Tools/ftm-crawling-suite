from abc import ABC

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor


class OrganizationUrlsSpider(CrawlSpider):
    """
    Given the seed website URLs, indexes all URLs from a given website and
    passes to the Mongo pipeline to be stored and scraped.
    """
    name = 'diffbot'
    allowed_domains = ['www.diffbot.com']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
    start_urls = ['https://www.carmax.com/cars/all']

    def __init__(self, **kwargs):
        """
        Initialize this spider with an instance of the MongoDB singleton as well as a
        link extractor.
        """
        # self.db = MongoDBSingleton.get_instance()
        super().__init__(**kwargs)
        self.link_extractor = LinkExtractor(unique=True)

    def start_requests(self):
        """
        Retrieves the URL seed for all organizations that exist.
        """
        organizations_collection = self.db.crawlingagent.organizations
        organizations = organizations_collection.find({"siteUrl": {"$ne": None}, "isDeleted": {"$ne": True}})
        if len(organizations) == 0:
            return print("There are no organizations to be fetched.")
        for organization in organizations:
            yield scrapy.Request(url=organization["siteUrl"], callback=self.parse_item)

    def parse_item(self, response):
        """
        After a request to the seed URL has been made, conduct a link extraction to retrieve
        all URLs from the site, passing them into a pipeline.
        """
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
