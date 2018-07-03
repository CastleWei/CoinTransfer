import gevent
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


# from multiprocessing import Process
from queue import Queue
output_queue = Queue()

def output_writer(q: Queue):
    path = 'output/result.json'
    # 重新启动程序后先清空
    with open(path, 'wb') as f:
        f.write(b'{}')

    while True:
        if q.not_empty:
            data = json.load(open(path, 'rb'))
            while not q.empty():
                it = q.get()
                data[it['name']] = it
            # print('data:', data)
            json.dump(data, open(path, 'wt'), indent=2)
            # open(path, 'wb').write(json.dumps(data))
        time.sleep(2)
        # TODO: 如何正确退出


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
        buy_amount = sch.src.can_buy(sch.coin, total_money)
        sell_money = sch.dst.can_sell(sch.coin, buy_amount)
        profit = sell_money - total_money

        result = dict(
            name=sch.name,
            repr=sch.repr,
            buy_amount=buy_amount,
            sell_money=sell_money,
            profit=profit,
            time=time.time() # TODO
        )

        global output_queue
        output_queue.put(result)
        # print(result)

        if profit > 2:
            # do the transfer
            pass

    else:
        print(sch.repr, ': failed to get info')

    gevent.sleep(1)

from threading import Thread
if __name__ == '__main__':
    # Process(target=output_writer, args=(output_queue,)).start()
    Thread(target=output_writer, args=(output_queue,)).start()
    while True:
        pool_size = len(schemes) / 3 + 1
        pool = gevent.pool.Pool(pool_size)
        # TODO: pool.imap_unordered
        for sch in schemes:
            pool.spawn(do_scheme, sch)
        pool.join()
        gevent.sleep(2)

