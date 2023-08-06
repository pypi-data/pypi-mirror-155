import time
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette_jwt import JWTAuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from dl2050utils.core import oget
from dl2050utils.env import config_load
from dl2050utils.log import AppLog
from dl2050utils.com import Notify, read_address_book
from dl2050utils.db import DB
from dl2050utils.mq import MQ
from dl2050utils.auth import Auth
from dl2050utils.restutils import HTTPException
from dl2050utils.restapp import App

class ASGI_Server():

    def __init__(self, name, path, routes, appstartup, perm, qs):
        cfg = config_load(name)
        LOG = AppLog(cfg)
        NOTIFY = Notify(cfg=cfg, address_book=read_address_book())
        dbname = oget(cfg, ['db','dbname'], 'postgres')
        db = DB(cfg=cfg, log=LOG, dbname=dbname)
        mq = MQ(LOG, db, qs, cfg=cfg)
        auth = Auth(cfg, LOG, NOTIFY, db)
        app = App(cfg, LOG, NOTIFY, db, mq, auth, path, routes, appstartup, perm)
        self.LOG,self.db,self.mq,self.auth,self.app = LOG,db,mq,auth,app
        self.port = oget(cfg, ['rest','port'], 5000)
        self.exception_handlers = {
            HTTPException: self.http_exception,
            404: self.http_exception,
            Exception: self.server_error_exception,
            500: self.server_error_exception,
        }
        auth_secret = cfg['rest']['auth_secret']
        self.middleware = [
            Middleware(RestStartMiddleware),
            Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], expose_headers=['*']),
            Middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=auth_secret, prefix='Bearer',
                       username_field='uid')),
            Middleware(RestEndMiddleware, LOG=self.LOG, auth=auth),
        ]
        self.routes = auth.get_routes()+app.get_routes()
        
    async def startup(self):
        if await self.db.startup(): raise('DB startup error')
        if await self.mq.startup(): self.LOG(3, 0, label='REST', label2='STARTUP', msg='MQ not available')
        if await self.auth.startup(): raise('Auth startup error')
        if await self.app.startup(): raise('App startup error')
        self.LOG(2, 0, label='REST', label2='STARTUP', msg=f'OK (port {self.port})')
        return False
            
    async def shutdown(self):
        self.LOG(2, 0, label='REST', label2='SHUTDOWN')
    
    async def http_exception(self, request, exc):
        request.state.error = True
        request.state.error = exc.detail
        return JSONResponse({'status': 'HTTP_EXCEPTION', 'error_msg': exc.detail}, status_code=exc.status_code)

    async def server_error_exception(self, request, exc):
        self.LOG(4, 0, label='REST', label2='SERVER_EXCEPTION', msg=exc.detail)
        return JSONResponse({'status': 'SERVER_EXCEPTION', 'error_msg': exc.detail}, status_code=exc.status_code)
        
    def run(self, port=None):
        rest = Starlette(
            debug=True,
            exception_handlers=self.exception_handlers,
            middleware=self.middleware,
            on_startup=[self.startup],
            on_shutdown=[self.shutdown],
            routes=self.routes,
        )
        port = port or self.port
        uvicorn.run(rest, port=port, host='0.0.0.0', log_level='critical')

class RestStartMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    async def dispatch(self, request, call_next):
        request.state.error = False
        request.state.t0 = time.time()
        return await call_next(request)

class RestEndMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, LOG=None, auth=None):
        super().__init__(app)
        self.LOG,self.auth=LOG,auth
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        url,uid,error,t = request.url.path,request.user.display_name,request.state.error,time.time()-request.state.t0
        if uid=='': uid=-1
        if request.state.error:
            self.LOG(4, t, label='REST', label2='HTTP_EXCEPTION', msg=request.state.error)
            return response
        if request.url.path not in ['/api/auth/is_auth', '/api/get_meta']:
            await self.auth.register_requests(url, uid, t, error)
        self.LOG(2, t, label='REST', label2=request.url.path, msg={'uid':uid})
        return response
