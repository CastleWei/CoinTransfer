import gevent_submodule as gsub
import gevent

def do_scheme():
    print('start do_scheme')
    g1 = gevent.spawn(gsub.req, 'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=103')
    g2 = gevent.spawn(gsub.req, 'https://openapi.dragonex.im/api/v1/market/buy/?symbol_id=104')
    gevent.joinall([g1, g2])
    print('return.. g1: %s, g2: %s'%(g1.value, g2.value))
    print('end do_scheme')

gevent.spawn(do_scheme).join()
print('end')