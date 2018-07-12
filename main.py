import gevent
import json
import time
import itertools

from coin_platforms.base_platform import BasePlatform
from utils import TransferScheme

platfroms = []

from coin_platforms.GateIO import GateIO
platfroms.append(GateIO)
from coin_platforms.DragonEx import DragonEx
platfroms.append(DragonEx)
from coin_platforms.Huobi import Huobi
platfroms.append(Huobi)

schemes = []

# 自动排列组合出所有可能的搬砖方案
for src in platfroms:
    for dst in platfroms:
        if src is dst:
            continue
        for coin in src.coin_infos:
            if coin in dst.coin_infos:
                sch = TransferScheme(src, coin, dst)
                schemes.append(sch)
                src.to_notify[coin].append(sch)
                dst.to_notify[coin].append(sch)


def update_scheme(sch: TransferScheme):
    # 相关的两个平台信息都有过第一次成功更新之后才可以计算
    # 没有update_time说明没有成功更新过，没有所需信息
    if ('update_time' not in sch.src.coin_infos[sch.coin]) or ('update_time' not in sch.dst.coin_infos[sch.coin]):
        return

    global shared_data
    total_money = shared_data['setting']['预备资金']

    buy_amount = sch.src.can_buy(sch.coin, total_money)
    sell_money = sch.dst.can_sell(sch.coin, buy_amount)
    profit = sell_money - total_money

    # print(sch.src.coin_infos[coin])
    result = dict(
        name=sch.name,
        repr=sch.repr,
        src_price=sch.src.coin_infos[sch.coin]['卖1价'],
        dst_price=sch.dst.coin_infos[sch.coin]['买1价'],
        profit=profit,
        time=time.time() # TODO
    )

    shared_data['result'][sch.name] = result

    if profit > 20:
        # do the transfer
        pass


def platform_watcher(plfm: BasePlatform):
    global shared_data
    last_request_time = 0
    while True:
        # 先查询汇率
        usdt_ok = plfm.query_usdt()
        gevent.sleep(1)
        while not usdt_ok:
            # 查询汇率直到成功
            usdt_ok = plfm.query_usdt()
            gevent.sleep(1)

        # 以平台为单位，各自进行请求，对每个网站请求不要太频繁
        for coin in plfm.coin_infos:
            last_request_time = time.time()

            req_ok = plfm.prepare_info(coin)
                
            # 本地的计算可以较频繁进行，因此每次得到新数据都重新计算一遍
            if req_ok:
                d = dict(
                    platform_name=plfm.platform_name,
                    coin=coin,
                    time=time.time(),
                    usdt_buy_price=plfm.usdt['price_to_buy'],
                    usdt_sell_price=plfm.usdt['price_to_sell'],
                )
                if '卖盘' in plfm.coin_infos[coin]:
                    d['卖盘'] = plfm.coin_infos[coin]['卖盘'][:5]
                    d['买盘'] = plfm.coin_infos[coin]['买盘'][:5]

                shared_data['market'][plfm.platform_name + '$$' + coin] = d
                # plfm_info = shared_data['market'].setdefault(plfm.platform_name, {})
                # plfm_info[coin] = d
                
                # 计算所有相关的scheme
                for sch in plfm.to_notify[coin]:
                    update_scheme(sch)

            delta_time = time.time() - last_request_time
            # 确保两次请求之间的间隔大约为timeliness
            timeliness = shared_data['setting']['查询间隔']
            if delta_time < timeliness:
                gevent.sleep(timeliness - delta_time)
            else:
                gevent.sleep(0)


if __name__ == '__main__':
    import signal, sys
    gevent.signal(signal.SIGINT, lambda: print('Exit by KeyboardInterrupt...') or sys.exit(0))

    shared_data = dict(
        market={},
        result={},
        setting={}
    )
    with open('local/setting.json', encoding='utf-8') as f:
        shared_data['setting'] = json.load(f)

    from output_server import run_server
    gevent.joinall(
        [gevent.spawn(run_server, shared_data)] +
        [gevent.spawn(platform_watcher, plfm) for plfm in platfroms]
    )
