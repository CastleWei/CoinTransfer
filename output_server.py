from gevent.pywsgi import WSGIServer
from urllib.parse import parse_qs
import json


_shared_data = {}
uris = ['/', '/main.js', '/main.css', '/minimal-table.css']


def application(env, start_response):
    path = env['PATH_INFO']

    # 对于result.json用共享内存的形式从主线程实时获取，避免不断读写硬盘
    if path == '/data.json':
        body = bytes(json.dumps(_shared_data), encoding='utf-8')
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

    if path == '/post-setting':
        content = env['wsgi.input'].read()
        d = parse_qs(content)
        
        psw = b''
        with open('local/password.txt') as f:
            psw = bytes(f.read(), encoding='utf8')

        if d.get(b'password', [''])[0] == psw:
            try:
                prepared_money = float(d[b'prepared_money'][0])
                operation_interval = float(d[b'operation_interval'][0])
                profit_threshold = float(d[b'profit_threshold'][0])
            except (ValueError, KeyError) as e:
                print('！接收到格式错误的POST信息', e)
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'invalid setting format']
            else:
                _shared_data['setting']['预备资金'] = prepared_money
                _shared_data['setting']['查询间隔'] = operation_interval
                _shared_data['setting']['操作阈值'] = profit_threshold

                with open('local/setting.json', 'wt', encoding='utf-8') as f:
                    json.dump(_shared_data['setting'], f, indent=4, ensure_ascii=False)

                print('设置被更改为:', content)
                
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'ok']
            

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'invalid password']


    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return [b'<h1>Not Found</h1>']


def run_server(shared_data):
    global _shared_data
    _shared_data = shared_data

    print('Serving on 8000...')
    WSGIServer(('', 8000), application).serve_forever()
