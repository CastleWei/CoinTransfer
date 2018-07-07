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

total_money = 1000


def update_scheme(sch: TransferScheme):
    # 相关的两个平台信息都有过第一次成功更新之后才可以计算
    # 没有update_time说明没有成功更新过，没有所需信息
    if 'update_time' not in sch.src.coin_infos[sch.coin] or 'update_time' not in sch.dst.coin_infos[sch.coin]:
        return

    global total_money
    buy_amount = sch.src.can_buy(sch.coin, total_money)
    sell_money = sch.dst.can_sell(sch.coin, buy_amount)
    profit = sell_money - total_money

    result = dict(
        name=sch.name,
        repr=sch.repr,
        total_money=total_money,
        buy_amount=buy_amount,
        sell_money=sell_money,
        profit=profit,
        time=time.time() # TODO
    )

    global shared_data
    data = shared_data['data']
    data[sch.name] = result

    if profit > 20:
        # do the transfer
        pass


def platform_watcher(plfm: BasePlatform):
    last_request_time = 0
    # 以平台为单位，各自进行请求，对每个网站请求不要太频繁
    for coin in itertools.cycle(plfm.coin_infos):
        last_request_time = time.time()

        req_ok = plfm.prepare_info(coin)
            
        # 本地的计算可以较频繁进行，因此每次得到新数据都重新计算一遍
        if req_ok:
            for sch in plfm.to_notify[coin]:
                update_scheme(sch)

        delta_time = time.time() - last_request_time
        # 确保两次请求之间的间隔大约为timeliness
        timeliness = 2
        if delta_time < timeliness:
            gevent.sleep(timeliness - delta_time)
        else:
            gevent.sleep(0)



from output_server import run_server
shared_data = {'data': {}}


if __name__ == '__main__':
    import signal, sys
    gevent.signal(signal.SIGINT, lambda: print('Exit by KeyboardInterrupt...') or sys.exit(0))

    gevent.joinall(
        [gevent.spawn(run_server, shared_data)] +
        [gevent.spawn(platform_watcher, plfm) for plfm in platfroms]
    )
