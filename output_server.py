from gevent.pywsgi import WSGIServer
from multiprocessing import Array


_mem = Array('b', 2)  # 这里的初始化只是形式而已，之后会覆盖

uris = ['/', '/main.js', '/main.css', '/minimal-table.css']


def application(env, start_response):
    path = env['PATH_INFO']

    # 对于result.json用共享内存的形式从主线程实时获取，避免不断读写硬盘
    if path == '/result.json':
        # 前四个字节是长度，网络字节序
        data = _mem[:]  # 先一次性读取，怕进程间不同步
        l = int.from_bytes(data[:4], 'big')
        body = bytes(data[4:l+4])
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


def run_server(mem):
    global _mem
    _mem = mem

    print('Serving on 8000...')
    WSGIServer(('', 8000), application).serve_forever()
