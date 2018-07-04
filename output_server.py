from gevent.pywsgi import WSGIServer


uris = ['/', '/main.js', '/main.css', '/minimal-table.css', '/result.json']


def application(env, start_response):
    path = env['PATH_INFO']

    if path in uris:
        if path == '/':
            path = '/index.html'

        content_type = 'text/html'
        if path.endswith('.json'):
            content_type = 'application/json'
        elif path.endswith('.js'):
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


def run_server():
    print('Serving on 8000...')
    WSGIServer(('', 8000), application).serve_forever()


if __name__ == '__main__':
    run_server()