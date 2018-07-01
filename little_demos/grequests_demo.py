import json
from pprint import pprint

urls = [
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=99',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=101',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=104',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=107',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=108',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=109',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=110',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=111',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=113',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=115',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=117',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=118',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=119',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=123',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=124',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=125',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=129',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=130',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=131',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=133',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=134',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=142',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=143',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=150',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=154',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=155',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=156',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=157',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=158',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=160',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=161',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=162',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=166',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1040103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1070103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1080103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1090103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1100103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1130103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1150103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1180103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1240103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1250103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1280103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1290103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1300103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1320103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1330103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1340103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1350103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1360103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1370103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1380103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1390103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1400103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1410103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1440103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1450103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1470103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1480103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1510103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1520103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1530103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1630103',
    'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=1650103'
]

import gevent
import grequests

def g(url):
    id = url[57:]
    print('start', id)
    r = grequests.get(url).send().response
    js = r.json()
    if js['data']:
        price1 = js['data'][0]
        print('done', id, price1)
    else:
        print('json fail:', id, r.text)
    gevent.sleep(1)

pool  = gevent.pool.Pool(3)
for url in urls:
    pool.spawn(g, url)
pool.join()