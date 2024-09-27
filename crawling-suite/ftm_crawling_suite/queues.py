from scrapy_redis.queue import PriorityQueue


class AltQueue(PriorityQueue):

    @property
    def key(self):
        return self.spider.name + ':requests'

    @key.setter
    def key(self, var):
        pass
