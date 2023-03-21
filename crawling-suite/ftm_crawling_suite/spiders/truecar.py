import json
import logging
from ftm_crawling_suite.items import RawDataRef

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TrueCarSpider(CrawlSpider):
    """
    Retrieves data from the TrueCar website.
    """
    name = 'truecar'
    allowed_domains = ['www.truecar.com']
    start_urls = [
        'https://www.truecar.com/used-cars-for-sale/listings/location-glassboro-nj/?page=1'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'ftm_crawling_suite.pipelines.duplicates.FilterDuplicatesPipeline': 100,
            'ftm_crawling_suite.pipelines.rawdataref.RawDataRefPipeline': 200,
        }
    }

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('a.page-link[data-test="Pagination-directional-next"]',)),
             callback="parse_item",
             process_request="add_header",
             follow=True),)

    def add_header(self, request, response):
        request.headers['Cookie'] = "_schn=_rrq2hhg; _ga=GA1.2.1865478527.1675451049; _gat_SITrackerQSI_38796=1; _gid=GA1.2.159392074.1675451049; _fbp=fb.1.1675451048934.2116940118; _ga_J3VWL05G5K=GS1.1.1675451048.1.1.1675451857.0.0.0; _gat_SITrackerQSI_87006=1; _pin_unauth=dWlkPVpHVTJaVGMyWmpVdE5XRXpaQzAwTW1GaExUbGhOR0l0WkdNMFlqVmxZMlZtT1RjeA; fs_uid=#G5Y78#4923899866042368:4867535831617536:::#63e3b8b8#/1706987048; utag_main=v_id:018618aa227a0002a8222d3f024e01075004a06d00b35$_sn:1$_se:38$_ss:0$_st:1675453655821$ses_id:1675451048571%3Bexp-session$_pn:4%3Bexp-session$dc_visit:1$dc_event:20%3Bexp-session$dc_region:us-east-1%3Bexp-session; _ga_XD4TBVCD03=GS1.1.1675451048.1.1.1675451855.0.0.0; _uetsid=8994a010a3f511edb4487f3b57085e64; _uetvid=8994a620a3f511ed945dcf33ada17250; _dd_s=rum=0&expire=1675452755189; flag-abt-ev-incentives-lp=true; flag-abt-fit-quiz-on-homepage=true; flag-abt-plus-landing-page-refresh=true; flag-abt-save-comparison-test=false; flag-abt-search-on-homepage=challenger1; flag-abt-shortlist-on-rankings-pages=false; flag-abt-showroom-vdp-conversion=control2; flag-abt-true-car-plus-global-nav-removal=control2; flag-trade-partner=true; tcPlusServiceArea=no; tcip=150.250.100.73; _gat_SITrackerQSI_29039=1; _gat_SITrackerQSI_18406=1; QSI_HistorySession=https%3A%2F%2Fwww.truecar.com%2Fused-cars-for-sale%2Flistings%2Flocation-glassboro-nj%2F~1675451050587%7Chttps%3A%2F%2Fwww.truecar.com%2Fused-cars-for-sale%2Flistings%2Flocation-glassboro-nj%2F%3Fpage%3D333~1675451110445%7Chttps%3A%2F%2Fwww.truecar.com%2Fused-cars-for-sale%2Flistings%2Flocation-glassboro-nj%2F~1675451300499%7Chttps%3A%2F%2Fwww.truecar.com%2Fused-cars-for-sale%2Flistings%2Flocation-glassboro-nj%2F%3FsearchRadius%3D5000~1675451789837; _sctr=1|1675400400000; _gcl_au=1.1.1177312274.1675451049; ln_or=eyI2MjU2NTIiOiJkIn0%3D; sa-user-id=s%253A.o6W7wkJsHSTU4%252BLlDruZ%252FwNjVcUZZMvakQpSatDoAgo; sa-user-id-v2=s%253A.o6W7wkJsHSTU4%252BLlDruZ%252FwNjVcUZZMvakQpSatDoAgo; _scid=8e9095bb-60ff-44ed-b19b-b978c6218d0b; tealium_test_field=Test_A; tc_v=55b8c393-3ba3-4736-9fc2-954c63b13c0d; u=rBEAEWPdWqKv/AARVFmuAg==; _abp_auth_p=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJiZGYxNzljZS1lN2IxLTQyZmEtODc1Ny04ZWEwYzNhMmYwYmIiLCJpYXQiOjE2NzU0NTEwNDMsImV4cCI6MTY5MTQ1MTA0MywianRpIjoiNGZmNGZmMzgtNzliYS00Mjk2LWI0MGUtOWEyMWMxMGFhMjU0IiwiYXV0aGVudGljYXRlZCI6ZmFsc2UsInByZXNldCI6eyJhZmZpbGlhdGlvbnMiOltdfSwiYXVkIjoiaHR0cHM6Ly93d3cudHJ1ZWNhci5jb20ifQ; _abp_auth_s=pD1wPn6qoyRjYB5ZY-hp9VcRmMg1kurXwUoW0ZyDE-w; referrer=ZTC0000000"
        request.headers['Host'] = "www.truecar.com"
        request.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        return request

    def parse_item(self, response):
        """
        Parse the page content by searching for a button to the next page and
        passing the data retrieved to the callback.
        """
        try:
            results = json.loads(response.css('script:contains("@context")::text').get())
            page_results = results[0]['vehicles']
            for i in range(0, len(page_results)):
                if "vehicleidentificationnumber" in page_results[i]:
                    item = RawDataRef()
                    item['raw'] = page_results[i]
                    item['dataRef'] = 'truecar'
                    item['collection'] = 'products'
                    item['uniqueId'] = page_results[i]["vehicleidentificationnumber"]
                    yield item
        except BaseException as E:
            print(E)
            self.log(message=f'Error while parsing data on page..', level=logging.WARNING)
