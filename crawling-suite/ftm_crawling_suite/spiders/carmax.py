import json
import logging
from urllib.request import Request
from ftm_crawling_suite.items import RawDataRef

from scrapy.spiders import CrawlSpider
import scrapy


class CarMaxSpider(CrawlSpider):
    """
    
    Crawls and retrieves car product data from the CarMax website.

    """
    name = 'carmax'
    allowed_domains = ['www.carmax.com']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
    start_urls = ['https://www.carmax.com/cars/all']
    custom_settings = {
        'ITEM_PIPELINES': {
            'ftm_crawling_suite.pipelines.duplicates.FilterDuplicatesPipeline': 100,
            'ftm_crawling_suite.pipelines.rawdataref.RawDataRefPipeline': 200,
        }
    }

    def start_requests(self):
        """
        Initialize the request, retrieve totals from the first API call and iterate in sequence.
        """
        yield scrapy.Request(url='https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fall&skip=0&take=1&zipCode=08103&radius=radius-nationwide&shipping=-1&sort=best-match&scoringProfile=BestMatchScoreVariant3&visitorID=401b1e29-61b5-454a-adb2-5644a4f98db4',
                             callback=self.recurse_api_calls)

    def recurse_api_calls(self, response):
        """
        Retrieves the total number of results from the primary API call. Then, calculates the
        number of iterations necessary to pull the data set and iterates.
        """
        total_count = response.json()['totalCount']
        num_iterations = round(total_count / 100)
        for i in range(0, num_iterations):
            yield scrapy.Request(url=f"https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fall&skip={i*100}&take=100&zipCode=08103&radius=radius-nationwide&shipping=-1&sort=best-match&scoringProfile=BestMatchScoreVariant3&visitorID=401b1e29-61b5-454a-adb2-5644a4f98db4",
                                 callback=self.parse)

    def parse(self, response):
        """
        Parses product data from the API response.
        """
        result = response.json()
        if 'items' in result and isinstance(result['items'], list) and len(result['items']) > 0:
            for i in range(0, len(result['items'])):
                item = RawDataRef()
                item['raw'] = result['items'][i]
                item['dataRef'] = 'carmax'
                item['collection'] = 'products'
                item['uniqueId'] = result['items'][i]["vin"]
                yield item
