from scrapy.spiders import CrawlSpider


class S3Spider(CrawlSpider):

    """
    Generic spider which exports results of the crawl to S3 as chunked
    gzip'd json-lines files.
    """

    # Original settings for reference.
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "ftm_crawling_suite.pipelines.DataTagPipeline": 200,
    #         "ftm_crawling_suite.custom_pipelines.s3.S3ExporterPipeline": 300
    #     },
    #     "SPIDER_MIDDLEWARES": {
    #         'ftm_crawling_suite.middlewares.FtmOffsiteMiddleware': 500,
    #         'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
    #     },
    #     'CONCURRENT_REQUESTS': 300,
    #     "DUPEFILTER_CLASS": "ftm_crawling_suite.spiders.organizationurls2.AltDupeFilter",
    #     "SCHEDULER_QUEUE_CLASS": "ftm_crawling_suite.queues.AltQueue",
    #     "DEPTH_LIMIT": None
    # }

    # Optimized settings for VM.
    custom_settings = {
        "ITEM_PIPELINES": {
            "ftm_crawling_suite.pipelines.DataTagPipeline": 200,
            "ftm_crawling_suite.custom_pipelines.s3.S3ExporterPipeline": 300
        },
        "SPIDER_MIDDLEWARES": {
            'ftm_crawling_suite.middlewares.FtmOffsiteMiddleware': 500,
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        },
        "DUPEFILTER_CLASS": "ftm_crawling_suite.spiders.organizationurls2.AltDupeFilter",
        "SCHEDULER_QUEUE_CLASS": "ftm_crawling_suite.queues.AltQueue",
        "DEPTH_LIMIT": None,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'CONCURRENT_REQUESTS_PER_IP': 8,

        # Enable AutoThrottle to manage request rates dynamically
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,  # Initial delay
        'AUTOTHROTTLE_MAX_DELAY': 10,  # Maximum delay
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,  # Average requests in parallel

        # Disable cookies
        'COOKIES_ENABLED': False,

        # Disable Telnet Console
        'TELNETCONSOLE_ENABLED': True,

        # Disable retries to reduce resource usage
        'RETRY_ENABLED': False,

        # Enable HTTP caching to reduce repeated requests
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,  # Cache indefinitely
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [500, 502, 503, 504, 408],

        # Adjust logging level
        'LOG_LEVEL': 'DEBUG'
    }

