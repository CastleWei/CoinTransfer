from abc import ABC, abstractmethod
from collections import defaultdict
import time
import gevent


class BasePlatform(ABC):
    platform_name = 'undefined'
    
    req_timeout = 3

    coin_infos = {}
    to_notify = defaultdict(list)

    @classmethod
    @abstractmethod
    def _request_info(cls, coin: str):
        pass

    @classmethod
    def prepare_info(cls, coin: str):
        inf = cls.coin_infos[coin]

        # TODO: 手续费也实时从网站请求
        # 发起请求获取数据
        req = gevent.spawn(cls._request_info, coin)
        try:
            req.join(cls.req_timeout)
            req.get()  # 如果有异常，重新抛出
        except gevent.Timeout:
            print('！超时：查询 %s 时超时' % cls.platform_name)
            return False
        except ValueError:
            print('！错误：查询 %s 时得到无效响应' % cls.platform_name)
            return False
        except KeyError:
            print('！错误：查询 %s 时得到的信息格式错误' % cls.platform_name)
            return False

        inf['update_time'] = time.time()  # 表明时效性，同时也表明有过第一次成功查询

        ## 以下为 cls._request_info() 的示例
        # url = 'https://data.gateio.io/api2/1/orderBook/%s_usdt' % coin
        # r = grequests.get(url).send().response
        # if not r: raise ValueError
        # d = r.json()
        # inf = cls.coin_infos[coin]
        # inf['卖盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['asks'])]
        # inf['卖盘'].reverse()
        # inf['买盘'] = [i for i in map(lambda x: (float(x[0]), float(x[1])), d['bids'])]
        # inf['卖1价'] = inf['卖盘'][0][0]
        # inf['买1价'] = inf['买盘'][0][0]
        
        # 返回成功
        return True


    @classmethod
    def can_buy(cls, coin: str, total_money):
        inf = cls.coin_infos[coin]
        # TODO: 测试
        return total_money / inf['卖1价'] * (1 - inf['交易手续费比例']) - inf['提现手续费定额']


    @classmethod
    def can_sell(cls, coin: str, amount):
        need_money = 0
        买盘 = cls.coin_infos[coin]['买盘']
        for price, volumn in 买盘:
            if volumn < amount:
                # 这一笔卖不完
                need_money += price * volumn
                amount -= volumn
            else:
                need_money += price * amount
                amount = 0
                break
        # TODO: 测试
        return need_money

