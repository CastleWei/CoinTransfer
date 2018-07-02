import gevent
import grequests

def req(url):
    print('gsub.req start:', url[-3:])
    r = grequests.get(url).send().response
    data = r.json()['data'][0]
    print('gsub.req ends:', url[-3:])
    return url[-3:] + str(data)