import gevent
import grequests
import json
import time

from utils import TransferScheme
from utils import Direction

platfroms = []

from coin_platforms import GateIO
platfroms.append(GateIO)
from coin_platforms import DragonEx
platfroms.append(DragonEx)
from coin_platforms import Huobi
platfroms.append(Huobi)

schemes = [
    TransferScheme(GateIO, 'btc', DragonEx),
    TransferScheme(DragonEx, 'btc', GateIO),
    TransferScheme(GateIO, 'eth', DragonEx),
    TransferScheme(DragonEx, 'eth', GateIO),
    TransferScheme(GateIO, 'btc', Huobi),
    TransferScheme(GateIO, 'eth', Huobi),
    TransferScheme(Huobi, 'eth', DragonEx),
]


from queue import Queue
output_queue = Queue()

def output_writer(q: Queue):
    path = 'output/result.json'
    # 重新启动程序后先清空
    with open(path, 'wb') as f:
        f.write('{}')

    while True:
        if q.not_empty:
            data = json.load(open(path, 'rb'))
            while q.not_empty:
                it = q.get()
                data[it['name']] = it
            json.dump(data, open(path, 'wb'))
        time.sleep(5)
        # TODO: 如何正确退出

from multiprocessing import Process
# !!!???
Process(target=output_writer, arg=(output_queue,)).start()


total_money = 1000

def do_scheme(sch):

    sch.src.timeliness = 5
    sch.src.req_timeout = 5
    sch.dst.timeliness = 5
    sch.dst.req_timeout = 5

    src_checker = gevent.spawn(sch.src.prepare_info, sch.coin, Direction.Buy)
    dst_checker = gevent.spawn(sch.dst.prepare_info, sch.coin, Direction.Sell)
    gevent.joinall([src_checker, dst_checker])

    if src_checker.value and dst_checker.value:
        global total_money
        buy_amount = sch.src.can_buy(total_money)
        sell_money = sch.dst.can_sell(buy_amount)
        profit = sell_money - total_money

        result = dict(
            name=sch.name,
            repr=sch.repr,
            profit=profit,
            time=time.time() # TODO
        )

        global output_queue
        output_queue.put(result)

        if profit > 2:
            # do the transfer
            pass

    else:
        print(sch.repr, ': failed to get info')

    gevent.sleep(1)


if __name__ == '__main__':
    while True:
        pool_size = len(schemes) / 3 + 1
        pool = gevent.pool.Pool(pool_size)
        for sch in schemes:
            pool.spawn(do_scheme, sch)
        pool.join()
        gevent.sleep(2)

