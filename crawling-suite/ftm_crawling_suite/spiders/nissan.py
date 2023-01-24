import json
import logging

import scrapy
from ftm_crawling_suite.items import RawDataRef
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


class NissanSpider(CrawlSpider):
    name = 'nissan'
    allowed_domains = ['nissanusa.com']
    start_urls = ['http://nissanusa.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'ftm_crawling_suite.pipelines.rawdataref.RawDataRefPipeline': 100,
            'ftm_crawling_suite.pipelines.nissan.NissanDataCleaningPipeline': 200,
            'ftm_crawling_suite.pipelines.cleanedproduct.CleanedProductPipeline': 300,
        }
    }

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('div.c_310-1 a',)),
             callback="parse_item",
             follow=True),)

    def parse_vehicle_specs(self, response):
        """For each vehicle type identified, navigate to the specs page and extract attributes such as trim,
        transmission types, drivetrain, and add-on accessories. The full data set of different trims and
        product types is stored in a JSON which can be parsed."""
        try:
            url_category_names_component = response.url.replace('https://www.nissanusa.com/vehicles/', '')\
                .replace('specs/compare-specs.html', '').split('/')
            vehicle_spec_regex = r"HELIOS.components.c059E= (.*);"
            # Produces an array of different cars with "grades" which are the trims. Within each
            # grade, there are different versions which include possible and potential specs
            # that are offered for that particular vehicle grade. Each version represents a product.
            vehicle_specs_raw = json.loads(response.css('script:contains("HELIOS.components.c059E=")::text')
                                           .re_first(vehicle_spec_regex))
            if vehicle_specs_raw is not None:
                # Grades are the "trim" attribute for that vehicle model.
                for trim, version in vehicle_specs_raw['grades'].items():
                    # Append the trim as well as the category names in the list of fields.
                    for uid, product in version['versions'].items():
                        raw_product = RawDataRef()
                        raw_product['dataRef'] = 'nissan-usa'
                        raw_product['collection'] = 'products'
                        raw_product['raw'] = product
                        raw_product['raw']['trim'] = trim.split('-')[1]
                        raw_product['raw']['categoryNames'] = url_category_names_component
                        raw_product['uniqueId'] = uid
                        yield raw_product
        except:
            self.log(f"Error while parsing data for page...", level=logging.WARNING)

    def parse_item(self, response):
        """First, index all menu item URLs which are the vehicles within their categories."""
        try:
            vehicle_product_name = response.url.replace('https://www.nissanusa.com/', '').replace('.html', '')
            yield Request(
                url=f"https://www.nissanusa.com/{vehicle_product_name}/specs/compare-specs.html",
                callback=self.parse_vehicle_specs)
        except:
            self.log(message=f'Error while parsing data on page..', level=logging.WARNING)
