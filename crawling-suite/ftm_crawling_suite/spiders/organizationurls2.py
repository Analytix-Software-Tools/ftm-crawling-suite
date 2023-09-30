from scrapy.signals import spider_idle
from scrapy.spiders import CrawlSpider
from scrapy_redis.connection import get_redis_from_settings
from scrapy.exceptions import CloseSpider, DontCloseSpider
from scrapy.spiders import Rule
from scrapy.dupefilters import RFPDupeFilter
from scrapy import Request
import pymongo
import re


class AltDupeFilter(RFPDupeFilter):
    @classmethod
    def from_spider(cls, spider):
        return cls()


class OrganizationHtmlSpider(CrawlSpider):
    allowed_domains = []
    name = 'organizationurls2'
    custom_settings = {
        "ITEM_PIPELINES": {
            "crawler.pipelines.DataTagPipeline": 200,
            "crawler.pipelines.MongoPipeline": 300
        },
        "SPIDER_MIDDLEWARES": {
            'crawler.middlewares.FtmOffsiteMiddleware': 500,
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,

        },
        "DUPEFILTER_CLASS": "ftm_crawling_suite.spiders.capability_spider.AltDupeFilter",
        "SCHEDULER_QUEUE_CLASS": "ftm_crawling_suite.queues.AltQueue",
        "DEPTH_LIMIT": 4
    }
    rules = [
        Rule(callback="parse_item", follow=True)
    ]
    index = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        # init redis and mongo client
        cls.server = get_redis_from_settings(crawler.settings)
        cls.client = pymongo.MongoClient(crawler.settings.get('MONGO_URI'))
        cls.db = cls.client[crawler.settings.get('MONGO_DATABASE', 'scrapy')]

        # load signal handler for spider_idle
        from_crawler = super(OrganizationHtmlSpider, cls).from_crawler
        spider = from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_went_idle, signal=spider_idle)

        return spider

    def pop_redis(self):

        # Pop the next company url in company_urls
        url = self.server.zpopmin('organizationurls', 1)
        # If there are none, wait until there are
        if url is None or len(url) < 1:
            return None
        url = url[0][0]
        url = url.decode('utf-8')

        if url == 'exit':
            raise CloseSpider('Exit signal recieved. Terminating...')
        # parse domain from url
        domain = re.search(r'(\.|/|^)([^\./]+\.[^\./]+)(/|$)', url)

        if domain is None:
            raise CloseSpider('Invalid URL in company URLs ' + url)

        # Update spider info
        self.allowed_domains = [domain.group(2)]
        self.name = domain.group(2)
        self.logger.info('Popped ' + url + ' from company_urls')
        self.index = 0

        # Return initial request
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
            item = CompanyWebsiteStringItem()
            item['domain'] = self.allowed_domains[0]
            item['sourceUrl'] = response.request.url
            item['string'] = text
            item['index'] = self.index
            self.index += 1
            return item
        except:
            pass

    def start_requests(self):
        valid = self.pop_redis()
        return [] if valid is None else [valid]

    def spider_went_idle(self):
        valid = self.pop_redis()
        if valid is not None:
            self.crawler.engine.slot.scheduler.df.fingerprints = set()
            self.crawler.engine.crawl(valid, self)
        raise DontCloseSpider('Awaiting new URLs in redis...')
