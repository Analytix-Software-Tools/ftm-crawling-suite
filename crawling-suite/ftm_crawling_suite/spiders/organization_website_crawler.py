from scrapy.signals import spider_idle
from scrapy.spiders import CrawlSpider
from scrapy_redis.connection import get_redis_from_settings
from scrapy.exceptions import CloseSpider, DontCloseSpider
from scrapy.spiders import Rule
from scrapy.dupefilters import RFPDupeFilter
from scrapy import Request
from ftm_crawling_suite.items import OrganizationHtml
import pymongo
import re

from ftm_crawling_suite.spiders.s3spider import S3Spider


class AltDupeFilter(RFPDupeFilter):
    @classmethod
    def from_spider(cls, spider):
        return cls()


class OrganizationWebsiteSpider(S3Spider):

    """
    Scrapes raw organization website with a feed export to S3.
    """

    allowed_domains = []

    name = 'organization_website_crawler'

    rules = [
        Rule(callback="parse_item", follow=True)
    ]
    index = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        # init redis
        cls.server = get_redis_from_settings(crawler.settings)

        # load signal handler for spider_idle
        from_crawler = super(OrganizationWebsiteSpider, cls).from_crawler
        spider = from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_went_idle, signal=spider_idle)

        return spider

    def pop_redis(self):
        """
        Pop the next url and validate it is a valid domain before
        firing the request.
        """

        url = self.server.zpopmin('organizationurls', 1)

        if url is None or len(url) < 1:
            return None
        url = url[0][0]
        url = url.decode('utf-8')

        if url == 'exit':
            raise CloseSpider('Exit signal recieved. Terminating...')

        domain = re.search(r'(\.|/|^)([^\./]+\.[^\./]+)(/|$)', url)

        if domain is None:
            raise CloseSpider('Invalid URL in company URLs ' + url)

        self.allowed_domains = [domain.group(2)]
        self.name = domain.group(2)
        self.logger.info('Popped ' + url + ' from organizationurls')
        self.index = 0

        return Request(
            url=url,
            callback=self._callback,
            errback=self._errback,
            meta=dict(rule=0, link_text=url)
        )

    def parse_item(self, response):
        """
        Accumulate the text for a particular item.
        """
        try:
            text = ''.join(response.xpath("//body/descendant-or-self::*[not(self::script)]").getall())
            text = re.sub(' +', ' ', text)
            text = text.replace('\t', '')
            text = text.replace('\n', '')
            item = OrganizationHtml()
            item['domain'] = self.allowed_domains[0]
            item['sourceUrl'] = response.request.url
            item['string'] = text
            item['index'] = self.index
            self.index += 1
            return item
        except:
            pass

    def start_requests(self):
        """
        Begin request urls.
        """
        valid = self.pop_redis()
        return [] if valid is None else [valid]

    def spider_went_idle(self):
        """
        Keep spider open on idle and check redis queue for next url.
        """
        valid = self.pop_redis()
        if valid is not None:
            self.crawler.engine.slot.scheduler.df.fingerprints = set()
            self.crawler.engine.crawl(valid)
        raise DontCloseSpider('Awaiting new URLs in redis...')
