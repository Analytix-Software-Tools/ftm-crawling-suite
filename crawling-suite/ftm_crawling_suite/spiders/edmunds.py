import json
import logging
from urllib.request import Request
from ftm_crawling_suite.items import RawDataRef

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import scrapy


class EdmundsSpider(CrawlSpider):
    """
    Retrieves data from the Edmunds website.
    """
    name = 'edmunds'
    allowed_domains = ['www.edmunds.com']
    start_urls = [
        'https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&pagenumber=1'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'ftm_crawling_suite.pipelines.duplicates.FilterDuplicatesPipeline': 100,
            'ftm_crawling_suite.pipelines.rawdataref.RawDataRefPipeline': 200,
        }
    }

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('a.pagination-btn[data-tracking-value="next"]',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        """
        Parse the page content by searching for a button to the next page and
        passing the data retrieved to the callback.
        """
        try:
            page_results = json.loads(response.css('script:contains("@context")::text').get())
            for i in range(0, len(page_results)):
                if "vehicleIdentificationNumber" in page_results[i]:
                    item = RawDataRef()
                    item['raw'] = page_results[i]
                    item['dataRef'] = 'edmunds'
                    item['collection'] = 'products'
                    item['uniqueId'] = page_results[i]["vehicleIdentificationNumber"]
                    yield item
        except BaseException as E:
            print(E)
            self.log(message=f'Error while parsing data on page..', level=logging.WARNING)
