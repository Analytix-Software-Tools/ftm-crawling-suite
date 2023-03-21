from scrapy.spiders import CrawlSpider

class OrganizationUrlsSpider(CrawlSpider):
    """
    Given the seed website URLs, indexes all URLs from a given website and
    passes to the Mongo pipeline to be stored and scraped.
    """
    name = 'diffbot'
    allowed_domains = ['www.diffbot.com']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
    start_urls = ['https://www.carmax.com/cars/all']
    custom_settings = {
        'ITEM_PIPELINES': {
            'ftm_crawling_suite.pipelines.duplicates.FilterDuplicatesPipeline': 100,
            'ftm_crawling_suite.pipelines.rawdataref.RawDataRefPipeline': 200,
        }
    }

    def parse_item(self):
        """
        Parses a given product from Diffbot.
        """

        pass
