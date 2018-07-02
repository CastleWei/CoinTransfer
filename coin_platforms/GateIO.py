from utils import Direction
import grequests

platform_name = 'GateIO'
url = 'api.gateio.io'
api_key = 'C53913A7-E09B-48E8-AAEC-976B5D3349C3'
secret_key = '3b8fce5fa9120750c2de8510fd5796f444e8fa9b9411ecba845f36fef242d563'

info = {}
support_coins = []

timeliness = 5
req_timeout = 5

def prepare_info(coin: str, buy_or_sell: Direction):
    pass

def can_buy(coin: str, total_money):
    pass

def can_sell(coin: str, amount):
    pass
