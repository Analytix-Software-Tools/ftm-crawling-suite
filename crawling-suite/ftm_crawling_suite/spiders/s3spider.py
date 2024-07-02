from scrapy.spiders import CrawlSpider


class S3Spider(CrawlSpider):

    """
    Generic spider which exports results of the crawl to S3 as chunked
    gzip'd json-lines files.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "ftm_crawling_suite.pipelines.DataTagPipeline": 200,
            "ftm_crawling_suite.custom_pipelines.s3.S3ExporterPipeline": 300
        },
        "SPIDER_MIDDLEWARES": {
            'ftm_crawling_suite.middlewares.FtmOffsiteMiddleware': 500,
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        },
        'CONCURRENT_REQUESTS': 300,
        "DUPEFILTER_CLASS": "ftm_crawling_suite.spiders.organizationurls2.AltDupeFilter",
        "SCHEDULER_QUEUE_CLASS": "ftm_crawling_suite.queues.AltQueue",
        "DEPTH_LIMIT": None
    }

    def __init__(self):
        super().__init__()
