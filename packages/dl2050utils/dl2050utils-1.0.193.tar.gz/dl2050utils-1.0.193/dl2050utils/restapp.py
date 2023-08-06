import time
from pathlib import Path
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.authentication import requires
from dl2050utils.core import oget
from dl2050utils.restutils import HTTPException, rest_ok, rest_error, rest_exception, get_meta, get_required_args,\
                                  get_required, get_optional_args, mk_key, get_hash, db_increase

class App():

    def __init__(self, cfg, LOG, NOTIFY, db, mq, auth, path, routes=[], appstartup=None, perm=None):
        self.cfg,self.LOG,self.NOTIFY,self.db,self.mq,self.auth = cfg,LOG,NOTIFY,db,mq,auth
        self.routes,self.appstartup,self.perm = routes,appstartup,perm
        self.d = {'LOG':LOG, 'path':path, 'db':db, 'mq':mq}
        self.fs_secret = oget(self.cfg,['fs','secret'])

    async def startup(self):
        model,meta = oget(self.cfg,['app','model']),None
        if model is not None: meta = await get_meta(self.db, model)
        self.d['meta'] = meta
        if self.appstartup is None: return False
        return await self.appstartup(self.d)

    def shutdown(self):
        self.LOG(2, 0, label='APP', label2='shutdown', msg='OK')
        return False   

    def get_routes(self):
        BASE_ROUTES = [
            Route('/api/get_meta', endpoint=self.get_meta, methods=['GET']),
            Route('/api/download_general', endpoint=self.download_general, methods=['GET']),
            Route('/api/download_user/{fname}', endpoint=self.download_user, methods=['GET']),
            Route('/api/download_req', endpoint=self.download_req, methods=['POST']),
            Route('/api/upload_req', endpoint=self.upload_req, methods=['POST']),
            Route('/api/publish_job', endpoint=self.publish_job, methods=['POST']),
            Route('/api/get_jobs', endpoint=self.get_jobs, methods=['POST']),
            Route('/api/get_pending_jobs', endpoint=self.get_pending_jobs, methods=['POST']),
            Route('/api/get_job', endpoint=self.get_job, methods=['POST']),
        ]
        APP_ROUTES = [Route(e, endpoint=self.app_route, methods=['POST']) for e in self.routes]
        return BASE_ROUTES + APP_ROUTES

    @requires('authenticated')
    async def get_meta(self, request):
        u = await self.auth.check_auth(request)
        return rest_ok(self.d['meta'])

    @requires('authenticated')
    async def download_general(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        fname = request.path_params['fname']
        path = self.d['path']
        p = Path(f'{path}/private/{uid}/{fname}')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=fname)

    @requires('authenticated')
    async def download_user(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        fname = request.path_params['fname']
        path = self.d['path']
        p = Path(f'{path}/tmp/{int(time.time())//86400}-{uid}-{fname}')
        if not p.is_file():
            raise HTTPException(404, detail=f'File not found')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=fname)

    @requires('authenticated')
    async def download_req(self, request):
        if not self.fs_secret:
            rest_exception(self.LOG, 'APP', 'upload_req', 'Upload secret not defined')
        u = await self.auth.check_auth(request)
        # db_increase(self.db, 'users', 'uid', u['uid'], 'uploads')
        data = await request.json()
        args = get_required_args(data,['bucket','fname'])
        self.perm(self.d, u, request.url.path, args)
        res = {**args, 'ts':int(time.time())}
        h = get_hash(res, self.fs_secret)
        res['h'] = h
        return rest_ok(res)

    @requires('authenticated')
    async def upload_req(self, request):
        if not self.fs_secret:
            rest_exception(self.LOG, 'APP', 'upload_req', 'Upload secret not defined')
        u = await self.auth.check_auth(request)
        # db_increase(self.db, 'users', 'uid', u['uid'], 'downloads')
        data = await request.json()
        args = get_required_args(data,['bucket','fname','size'])
        self.perm(self.d, u, request.url.path, args)
        res = {**args, 'ts':int(time.time())}
        h = get_hash(res, self.fs_secret)
        res['h'] = h
        return rest_ok(res)

    @requires('authenticated')
    async def publish_job(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        data = await request.json()
        args = get_required_args(data,['q','payload'])
        q,payload = args['q'],args['payload']
        self.perm(self.d, u, request.url.path, args)
        jid = await self.mq.publish(q, uid, payload)
        if jid is None :
            return rest_error(self.LOG, 'APP', 'publish_job', '')
        self.LOG(2, 0, label='APP', label2='publish_job',  msg={'jid':jid, 'uid':uid, 'q':q})
        return rest_ok({'jid': jid})

    @requires('authenticated')
    async def get_jobs(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        data = await request.json()
        kwargs = get_optional_args(data,['jstatus'])
        jobs = await self.mq.get_jobs({uid:uid,**kwargs})
        return rest_ok(jobs)

    @requires('authenticated')
    async def get_pending_jobs(self, request):
        u = await self.auth.check_auth(request)
        jobs = await self.mq.get_pending_jobs(u['uid'])
        return rest_ok(jobs)

    @requires('authenticated')
    async def get_job(self, request):
        u = await self.auth.check_auth(request)
        data = await request.json()
        [jid] = get_required(data,['jid'])
        job = await self.mq.get_job(jid)
        return rest_ok(job)

    @requires('authenticated')
    async def app_route(self, request):
        if request.url.path not in self.routes:
            raise HTTPException(400, detail=f'App route not available')
        d = self.routes[request.url.path]
        f,args,kwargs = d['f'],d['args'],d['kwargs']
        u = await self.auth.check_auth(request)
        data = await request.json()
        args2 = get_required_args(data, args)
        kwargs2 = get_optional_args(data, args, kwargs)
        self.perm(self.d, u, request.url.path, {**args2, **kwargs2})
        res = await f(self.d, u, *[args2[e] for e in args2], **kwargs2)
        return rest_ok(res)
