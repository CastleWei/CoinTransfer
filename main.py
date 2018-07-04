import gevent
import json
import time
import itertools

from utils import TransferScheme
from utils import Direction

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
        for coin in src.infos:
            if coin in dst.infos:
                schemes.append(TransferScheme(src, coin, dst))

total_money = 1000

def do_scheme(sch):

    sch.src.timeliness = sch.dst.timeliness = 2
    sch.src.req_timeout = sch.dst.req_timeout = 2

    src_checker = gevent.spawn(sch.src.prepare_info, sch.coin, Direction.Buy)
    dst_checker = gevent.spawn(sch.dst.prepare_info, sch.coin, Direction.Sell)
    gevent.joinall([src_checker, dst_checker])

    if src_checker.value and dst_checker.value:
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

        global data, mem
        data[result['name']] = result
        output_data = bytes(json.dumps(data), encoding='utf-8')
        l = len(output_data)
        to_arr = l.to_bytes(4, 'big') + output_data
        mem[:l+4] = to_arr  # 一次性写入，怕进程间不同步

        if profit > 2:
            # do the transfer
            pass

    else:
        print(sch.repr, ': failed to get info')

    gevent.sleep(1)


from output_server import run_server
from multiprocessing import Process, Value, Array
# 对于result.json用共享内存的形式给服务器进程，避免不断读写硬盘
# 前四个字节放长度，后面接数据
data = {}
mem = Array('B', 1000000)  # 预留约1MB的内存


if __name__ == '__main__':
    Process(target=run_server, args=(mem,)).start()

    pool_size = len(schemes) / 3 + 1
    pool = gevent.pool.Pool(pool_size)
    result = pool.imap_unordered(do_scheme, itertools.cycle(schemes))
    for r in result:
        # 只有不断调用迭代器消耗掉结果，imap才会继续往下执行
        pass

