from multiprocessing import Process, Value, Array
import json

def f(a):
    d = {
        "GateIO$$eth$$Huobi": {
            "name": "GateIO$$eth$$Huobi",
            "repr": "GateIO --> eth --> Huobi",
            "total_money": 1000,
            "buy_amount": 2.1028850836656745,
            "sell_money": 995.613858010677,
            "profit": -4.38614198932305,
            "time": 1530719240.2837176
        },
        "GateIO$$btc$$Huobi": {
            "name": "GateIO$$btc$$Huobi",
            "repr": "GateIO --> btc --> Huobi",
            "total_money": 1000,
            "buy_amount": 0.1485057173203422,
            "sell_money": 992.2706514193305,
            "profit": -7.729348580669466,
            "time": 1530719239.2063675
        },
        "GateIO$$btc$$DragonEx": {
            "name": "GateIO$$btc$$DragonEx",
            "repr": "GateIO --> btc --> DragonEx",
            "total_money": 1000,
            "buy_amount": 0.1485057173203422,
            "sell_money": 1015.7184746833847,
            "profit": 15.71847468338467,
            "time": 1530719237.78383
        },
        "GateIO$$eth$$DragonEx": {
            "name": "GateIO$$eth$$DragonEx",
            "repr": "GateIO --> eth --> DragonEx",
            "total_money": 1000,
            "buy_amount": 2.1028850836656745,
            "sell_money": 1022.2372191698844,
            "profit": 22.237219169884384,
            "time": 1530719238.9685657
        },
        "DragonEx$$btc$$GateIO": {
            "name": "DragonEx$$btc$$GateIO",
            "repr": "DragonEx --> btc --> GateIO",
            "total_money": 1000,
            "buy_amount": 0.14412304201860276,
            "sell_money": 961.4082279267639,
            "profit": -38.59177207323614,
            "time": 1530719240.425911
        },
        "DragonEx$$eth$$GateIO": {
            "name": "DragonEx$$eth$$GateIO",
            "repr": "DragonEx --> eth --> GateIO",
            "total_money": 1000,
            "buy_amount": 2.0299373955886253,
            "sell_money": 960.2009868613314,
            "profit": -39.799013138668556,
            "time": 1530719239.263745
        },
        "DragonEx$$btc$$Huobi": {
            "name": "DragonEx$$btc$$Huobi",
            "repr": "DragonEx --> btc --> Huobi",
            "total_money": 1000,
            "buy_amount": 0.14412304201860276,
            "sell_money": 962.9869298556981,
            "profit": -37.01307014430188,
            "time": 1530719240.443924
        },
        "DragonEx$$eth$$Huobi": {
            "name": "DragonEx$$eth$$Huobi",
            "repr": "DragonEx --> eth --> Huobi",
            "total_money": 1000,
            "buy_amount": 2.0299373955886253,
            "sell_money": 961.2603343070376,
            "profit": -38.739665692962376,
            "time": 1530719236.7779884
        },
        "Huobi$$btc$$GateIO": {
            "name": "Huobi$$btc$$GateIO",
            "repr": "Huobi --> btc --> GateIO",
            "total_money": 1000,
            "buy_amount": 0.14535402140940512,
            "sell_money": 969.6190943494998,
            "profit": -30.380905650500154,
            "time": 1530719237.86427
        },
        "Huobi$$eth$$GateIO": {
            "name": "Huobi$$eth$$GateIO",
            "repr": "Huobi --> eth --> GateIO",
            "total_money": 1000,
            "buy_amount": 2.0971745281026983,
            "sell_money": 992.0867032831384,
            "profit": -7.913296716861623,
            "time": 1530719236.8285787
        },
        "Huobi$$btc$$DragonEx": {
            "name": "Huobi$$btc$$DragonEx",
            "repr": "Huobi --> btc --> DragonEx",
            "total_money": 1000,
            "buy_amount": 0.14535402140940512,
            "sell_money": 994.1680397180589,
            "profit": -5.831960281941065,
            "time": 1530719238.2590418
        },
        "Huobi$$eth$$DragonEx": {
            "name": "Huobi$$eth$$DragonEx",
            "repr": "Huobi --> eth --> DragonEx",
            "total_money": 1000,
            "buy_amount": 2.0971745281026983,
            "sell_money": 1019.4613181107217,
            "profit": 19.461318110721663,
            "time": 1530719237.2923617
        }
    }
    jsbytes = bytes(json.dumps(d), encoding='utf8')
    l = len(jsbytes)
    l+=1
    print('##############################',l)
    to_arr = l.to_bytes(4,'big') + jsbytes + b'a'
    a[:l+4] = to_arr
    

if __name__ == '__main__':

    arr = Array('B', 3000)

    p = Process(target=f, args=(arr,))
    p.start()
    p.join()

    print(arr[:4])
    len = int.from_bytes(arr[:4], 'big')
    print(len)
    res = bytes(arr[4:len+4])

    print(type(res), res)