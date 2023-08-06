import time
import cgi
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from dl2050utils.restutils import get_required_args, get_optional_args

class Handler(BaseHTTPRequestHandler):
    
    def log_message(self, format, line, return_code, _):
        msg = f'{self.command} {return_code}'
        if self.error: msg+=f' {self.error}'
        msg += f' {self.client_address}'
        t = self.t0 if hasattr(self, 't0') else 0
        level = 2 if return_code=='200' else 4
        self.LOG(level, time.time()-t, label='WSGIServer', label2=self.path, msg=msg)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self.t0 = time.time()
        self._set_headers()
        
    def do_GET(self):
        self.t0 = time.time()
        self.send_response(400)
        self.end_headers()

    def do_POST(self):
        try:
            self.t0 = time.time()
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype!='application/json':
                raise Exception('Content-type error')
            if self.path not in self.routes:
                raise Exception('Invalid route')
            length = int(self.headers.get('content-length'))
            payload = json.loads(self.rfile.read(length))
            route = self.routes[self.path]
            f,args,kwargs = route['f'],route['args'],route['kwargs']
            args2 = get_required_args(payload, args)
            kwargs2 = get_optional_args(payload, args, kwargs)
            res = f(self.d, *[args2[e] for e in args2], **kwargs2)
            res = json.dumps(res)
            res = res.encode()
        except Exception as err:
            self.error = str(err)
            self.send_response(400)
            self.send_header('Content-type','application/json')
            self.end_headers()
            res = {'error': str(err)}
            res = json.dumps(res)
            res = res.encode()
            self.wfile.write(res)
            return
        self._set_headers()
        self.wfile.write(res)

def HandlerFactory(routes, d):
    class ExtendedHandler(Handler):
        def __init__(self, *args, **kwargs):
            super(ExtendedHandler, self).__init__(*args, **kwargs)
    ExtendedHandler.routes = routes
    ExtendedHandler.d = d
    ExtendedHandler.LOG = d['LOG']
    ExtendedHandler.error = None
    return ExtendedHandler

class WSGIServer():
    def __init__(self, routes, startup, d={}, secret=None, host='', port=6000):
        self.routes,self.startup = routes,startup
        self.secret,self.host,self.port = secret, host,port
        self.d = d
        self.LOG = d['LOG']
        
    def run(self, host='', port=6000):
        try:
            if self.startup(self.d):
                return True
        except Exception as err:
            self.LOG(4, 0, label='WSGIServer', label2='STARTUP EXCEPTION', msg=str(err))
            raise RuntimeError('MDB STARTUP EXCEPTION')
        Handler = HandlerFactory(self.routes, self.d)
        httpd = HTTPServer((host, port), Handler)
        self.LOG(2, 0, label='WSGIServer', label2='RUN', msg=f'MDB listenning on {self.port}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
