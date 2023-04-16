from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ftm_crawling_suite.items import ProductItem


class NissanSpider(CrawlSpider):
    """
    Crawls Cars.com.
    """
    
    name = "nissan"
    start_urls = ["https://nissanusa.com/"]
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36'
    
    rules = (
        Rule(
            LinkExtractor(restrict_css=[
                "a[href*='/vehicles/']"
            ]),
            # callback="parse"
        ),
        Rule(
            LinkExtractor(allow='/comare-specs.html'),
            callback='parse_product_page'
        ),
    )

    def parse_product_page(self, response):
        """
        When a product page is encountered, route the request
        to the "specs" page and extract all details.
        """
        product = ProductItem()
        
        product['name'] = ""
        product['description'] = ""
        
        attribute_values = []
        pass
