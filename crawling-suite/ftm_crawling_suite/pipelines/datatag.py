import os
from datetime import datetime


class DataTagPipeline:

    def process_item(self, item, spider):
        item['host'] = os.uname()[1]
        item['last_updated'] = datetime.now()
        yield item