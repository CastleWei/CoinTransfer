from gevent.pywsgi import WSGIServer
import json


_data_wrapper = {'data': {}}
uris = ['/', '/main.js', '/main.css', '/minimal-table.css']


def application(env, start_response):
    path = env['PATH_INFO']

    # 对于result.json用共享内存的形式从主线程实时获取，避免不断读写硬盘
    if path == '/result.json':
        body = bytes(json.dumps(_data_wrapper['data']), encoding='utf-8')
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [body]

    if path in uris:
        if path == '/':
            path = '/index.html'

        content_type = 'text/html'
        if path.endswith('.js'):
            content_type = 'application/x-javascript'
        elif path.endswith('.css'):
            content_type = 'text/css'

        body = b''
        with open('./output' + path, 'rb') as f:
            body = f.read()
        start_response('200 OK', [('Content-Type', content_type)])
        return [body]

    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return [b'<h1>Not Found</h1>']


def run_server(data_wrapper):
    global _data_wrapper
    _data_wrapper = data_wrapper
    
    print('Serving on 8000...')
    WSGIServer(('', 8000), application).serve_forever()
