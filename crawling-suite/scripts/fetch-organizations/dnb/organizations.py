import ast
import json
import operator
import random
import uuid
import re

from pymongo import MongoClient

import urllib3

# Strategy: First, get the totals for a blank search query.
# Then, iterate while the index is less than the total and
# retrieve each document by iterating thru the pages with
# a search query that progressively adds more characters
# from a to z.

US_ORGANIZATION_TOTAL = 557949
RESULTS_PER_PAGE = 50

abc = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
]


def generate_search_string(num_letters=2):
    """Generate a random two-character search string for each
    number of letters allotted. This will cover up to 40 pages of search
    results. When 40 has been hit, rotate the search string.
    """
    random_char_list = []
    for i in range(0, num_letters):
        random_char_list.append(abc[random.Random().randint(0, len(abc) - 1)])
    return ''.join(random_char_list)


def get_organizations_recursive(random_search, page=0, organizations={}):
    """Retrieves all US-based organizations from DNB recursively. Maps the results
    onto a dict, which will filter out any duplicates.
    """
    try:
        if len(organizations) >= US_ORGANIZATION_TOTAL:
            with open('data.py', 'w+') as file:
                file.write(str(organizations.values()))
            return organizations
        print(len(organizations))
        http = urllib3.PoolManager()
        result = http.request('GET',
                              f'https://www.dnb.com/apps/dnb/servlets/CompanySearchServlet?countryIsoAlphaTwoCode=us&familyTreeRolesPlayed=9141&pageNumber={page}&pageSize={RESULTS_PER_PAGE}&resourcePath=%2Fcontent%2Fdnb-us%2Fen%2Fhome%2Fsite-search-results%2Fjcr:content%2Fcontent-ipar-cta%2Fsinglepagesearch&returnNav=true&searchTerm={random_search}&token=eyJwNCI6IlM1NU9xekdQYnhONzBTcXpKMWpsa0dMTE5KSUZPSU1ISUgiLCJwMiI6NSwicDMiOjM0LCJwMSI6MTY2ODQzMDkzNzIzMn0%3D',
                              headers={
                                  'Cookie': '_fbp=fb.1.1668479946677.658670102; s_sq=%5B%5BB%5D%5D; _gat_ncAudienceInsightsGa=1; _biz_nA=4; _biz_pendingA=%5B%5D; _st_l=38.600|8005269018,8442628785,,+18442628785,0,1668480546.8662583217,8554480107,,+18554480107,0,1668469957.8664733932,8556000839,,+18556000839,0,1668480545|1931427245.9912000545.18442628785.47512096806; AMCVS_8E4767C25245B0B80A490D4C%40AdobeOrg=1; AMCV_8E4767C25245B0B80A490D4C%40AdobeOrg=-1124106680%7CMCIDTS%7C19312%7CMCMID%7C67877514452979733934510233827867914803%7CMCAAMLH-1669084746%7C7%7CMCAAMB-1669084746%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1668487146s%7CNONE%7CvVersion%7C5.2.0; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+14+2022+21%3A39%3A06+GMT-0500+(EST)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=e203574d-8a00-4985-92f5-fd0ae515fad5&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=US%3BNJ; SSOD=ANZzAAAAEgAjzDMABAAAAGDScmPJ-3JjAQAAAA; __exponea_etc__=05e1ea8a-568e-4759-a328-a8985ec1c713; __exponea_time2__=0.0031843185424804688; __ncuid=b07144e2-4cf3-4f8b-92db-6116999f4acc; _biz_flagsA=%7B%22Version%22%3A1%2C%22Ecid%22%3A%22-1102508276%22%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _biz_sid=3e2671; _biz_uid=eb4eeaf4efb544b7c0b0895b9350ecfb; _dc_gtm_UA-18184345-1=1; _ga=GA1.2.453465202.1668479946; _ga_K0F9RX4KM4=GS1.1.1668479946.1.0.1668479946.0.0.0; _gat_UA-19892859-28=1; _gcl_au=1.1.442505096.1668479946; _gid=GA1.2.718321944.1668479946; _hjAbsoluteSessionInProgress=1; _hjFirstSeen=1; _hjSessionUser_1097690=eyJpZCI6ImU2NmMzMzcyLWY3MDEtNTYyMC05ZDZkLWE2OGFjMTdhYzBmNyIsImNyZWF0ZWQiOjE2Njg0Nzk5NDY2ODMsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_1097690=eyJpZCI6ImIwMTE4YzQ5LWNmOTUtNGNkMS04MmU4LTJiYjU2MzhhNDU4NSIsImNyZWF0ZWQiOjE2Njg0Nzk5NDY3NTYsImluU2FtcGxlIjpmYWxzZX0=; _mkto_trk=id:080-UQJ-704&token:_mch-dnb.com-1668479946893-92604; _mkto_trk_http=id:080-UQJ-704&token:_mch-dnb.com-1668469348763-75142; _st_bid=0120aab0-6476-11ed-913a-7354571d596c; _uetsid=ffa71720647511ed9d63717649ef387c; _uetvid=ffa74270647511edbceea536a6aeeb37; bm_sv=8E4000B95355682AD0A2A1A97BDC3516~YAAQzZw6F70GSXGEAQAAAJAneRHVP7EneBMWYzBL0l0rT38JFCUoae3/PHkPzJT8lXpH6PmSRKby5YoLUsnyrkeCVaDS59+rSwLfZ5ERGjoU0qRGydqzDQ5rr3oXAHGQ9vpTq6LR5+nYHk3MaM8kbDXORs9upOSPmsNBn7tPZpXBlsX+narCpqBJq23C7a7gL9RQbNcskgveVfqhjBQ6FHp1y8h9Pj259nQh1GkNVhcObGIjNI5+mqmo4cieIw==~1; s_cc=true; s_nr30=1668479946462-New; _st=0120aab0-6476-11ed-913a-7354571d596c.0122f4a0-6476-11ed-913a-7354571d596c....0....1668480546.1668490746.600.10800.30.0....1....1.10,11..dnb^com.UA-18184345-1.1237074323^1668469348.38.; ln_or=d; HID=1668479946377; _hjIncludedInSessionSample=0; _sp_id.2291=fb9d52ea-4af4-48a2-9010-7c8f74fc0612.1668479947.1.1668479947.1668479947.f12b27d3-d0dc-448d-9e14-de1776abd318; _sp_ses.2291=*; drift_aid=c985ea05-ac3b-4781-90f4-b4438a9d5a1d; drift_campaign_refresh=fb5249b3-5bba-4001-a762-5cdcbfc1d2ad; driftt_aid=c985ea05-ac3b-4781-90f4-b4438a9d5a1d; tbw_bw_sd=1668479947; tbw_bw_uid=bito.AAGW-U7G5RwAAB-Fqg7avA; ak_bmsc=DE11B50A10EB3C4F64EE46FB90009243~000000000000000000000000000000~YAAQzZw6F3gFSXGEAQAA5YMneREMR4yJfQt+ihpAyjczkaf+eHBstgpLpmHdMPr8iaEWdfWeBajF5U0lmMcfDmL2mou5dbVa49juB8gp7cx2JQmhq2En4CCN06tRo2cSQ4QM/sZADFHqdXjtWYQt5uYIas5lmDSpLNVaYt6Y2dMFeGZJKVLtCAAD8L2c5vV2wr1wWRUaNVYAvdZAWNabVHJW/3G2GKe+/ewCN9jb6bc7kc3aUUW2dTqBZOH2lu0icT45zw5N0m04jNCkto2c1FrpCMWnqpyLfR/dFF1wSQmvzvdsBv+j+t+JlEyuMkY+IJeAoJBEqPUG5QqqIDVqgm3BsQxkVs8CvR12UYCiwVJeqY8fjKinv+6geQOIuq81w03A40t4RfGu5I0DS83inoONhclQ9wen+rRCW9MWL9uZkGatVeGfKqxndPrp4S2bJivYv8w/K82cbUI=; SSLB=1; SSID=CQBW3h2MAAAAAABg0nJjr8EBBmDScmMCAAAAAACMYJpjpvtyYwB-5Z0WAQFARCQApvtyYwEAxxUBAVo1JACm-3JjAQCJEAEBDsIjAKb7cmMBAMQWAQM2RiQAYNJyYwIAXw8BAeWmIwCm-3JjAQClEgEBV_gjAKb7cmMBANYTAQHQDSQApvtyYwEA8RABAWvwIwCm-3JjAQCTFgEBckMkAKb7cmMBAIYVAQNJMCQAYNJyYwIA; SSRT=pvtyYwADAA; SSSC=644.G7166021266959352239.2|69471.2336485:69769.2343438:69873.2355307:70309.2357335:70614.2362832:71046.2371657:71111.2372954:71315.2376562:71325.2376768:71364.2377270; OptanonAlertBoxClosed=2022-11-14T23:42:38.019Z; language_preference=en-us; site_preference=en-us',
                                  'Accept': 'application/json, text/plain, */*',
                                  'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
                              })
        organizations_body = json.loads(result.data.decode('utf-8'))
        if 'companies' in organizations_body:
            if organizations_body['totalMatchedResults'] == 0 or len(organizations_body['companies']) == 0:
                return get_organizations_recursive(generate_search_string(), 0, organizations)
            new_organizations = {**organizations}
            for organization in organizations_body['companies']:
                if organization['duns'] not in new_organizations:
                    new_organizations[organization['duns']] = organization
            if len(new_organizations.keys()) < organizations_body['totalMatchedResults']:
                return get_organizations_recursive(random_search, page + 1, new_organizations)
            return get_organizations_recursive(generate_search_string(), 0, new_organizations)
        else:
            print('Something happened, so we logged progress and continued the request.')
            with open(f'{uuid.uuid4()}.py', 'w+') as file:
                file.write(str(organizations.values()))
            return get_organizations_recursive(generate_search_string(), 0, organizations)
    except:
        print('An error actually happened, so we logged before stuff hit the fan.')
        with open(f'error-{uuid.uuid4()}.py', 'w+') as file:
            file.write(str(organizations.values()))
        return get_organizations_recursive(generate_search_string(), 0, organizations)


def import_raw_data():
    """Imports raw data into the collection.
    """
    client = MongoClient('mongodb+srv://admin:eky0PQyN3cd71WwY@cluster0.illqh.mongodb.net')
    with open('testdfe6d7c0-d55d-4cc1-a8cf-fc4ea4a6e578.py', "r") as data:
        raw_json = ast.literal_eval(data.read())
        new_documents = map(lambda x: {"dataRef": "dnb", "collection": "organizations", "raw": {**x}}, raw_json)
        client['crawlingagent'].raw_data.insert_many(new_documents)
        print('Mongo insertion completed.')

# get_organizations_recursive(generate_search_string())
import_raw_data()
