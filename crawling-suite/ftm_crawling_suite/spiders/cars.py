import json
import logging
from urllib.request import Request
from ftm_crawling_suite.items import RawDataRef

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import chompjs
import scrapy


class CarsSpider(CrawlSpider):
    """Represents a web crawler designed to crawl the CarsSpider pages
    and extract information about the cars they provide.
    """
    name = 'cars'
    allowed_domains = ['www.cars.com']
    start_urls = ['https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%5D=&models%5B%5D=&list_price_max=&page_size=100&maximum_distance=all&zip=']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('a.sds-pagination__control',)),
             callback="parse_item",
             follow=True),)


    listing_id_to_raw = {}


    def parse_vehicle_details(self, response):
        """Fetches the item details of the vehicle. The detail page includes more detailed
        attributes of the vehicle such as any addons, the transmission and engine types, and
        more. Further, this also lists the seller of the particular item.
        """
        initial_activity_regex = r'window.CARS\["initialActivity"\] = (.*)'
        dispatcher_regex = r'"CarsWeb.ListingController.show": (.*)}\)'
        activity_search_results = json.loads(response.css('script:contains("initialActivity")::text').re_first(initial_activity_regex))
        detail_search_results = json.loads(response.css('script:contains("dispatcher")::text').re_first(dispatcher_regex))
        item = RawDataRef()
        item['raw'] = {"initialActivity": activity_search_results, "detail": detail_search_results}
        item['dataRef'] = 'carsdotcom'
        item['collection'] = 'services'
        item['uniqueId'] = activity_search_results["listing_id"]
        yield item

    def parse_item(self, response):
        """Grab and extract all JavaScript data from the field and then
        navigate to the next page.
        """
        try:
            # Parse search-live-content with data attributes for the search data.
            search_results = json.loads(response.css('div#search-live-content::attr(data-site-activity)').get())
            for i in range(0, len(search_results['vehicleArray'])):
                yield Request(url=f"https://www.cars.com/vehicledetail/{search_results['vehicleArray'][i]['listing_id']}/", callback=self.parse_vehicle_details)
        except:
            self.log(message=f'Error while parsing data on page..',level=logging.WARNING)
