import uuid
from abc import ABC

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from ftm_crawling_suite.items import OrganizationHtml


class OrganizationUrlsSpider(RedisCrawlSpider):
    """
    Polls redis for websites to crawl and extracts the content to mongo.
    """
    name = 'organizationurls'
    collection = "organization_html"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"

    custom_settings = {
        "ITEM_PIPELINES": {
            "ftm_crawling_suite.pipelines.DataTagPipeline": 200,
            "ftm_crawling_suite.pipelines.MongoPipeline": 400,
        },
        "DEPTH_LIMIT": 4,
        "collection": "organization_html"
    }

    rules = [
        Rule(callback="parse", follow=True)
    ]

    def parse(self, response, **kwargs):
        html = response.xpath('//body').get()
        # result_doc = OrganizationHtml()
        # result_doc['domain'] = response.url
        # result_doc['pageUrl'] = response.url
        # result_doc['pid'] = str(uuid.uuid4())
        # result_doc['rawHtml'] = html
        yield {
            "domain": response.url,
            "pageUrl": response.url,
            "pid": str(uuid.uuid4()),
            "rawHtml": html
        }
