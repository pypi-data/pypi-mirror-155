import asyncio
import sys
from dl2050utils.core import oget,listify
from dl2050utils.env import config_load
from dl2050utils.log import AppLog
from dl2050utils.db import DB
from dl2050utils.mq import MQ
from dl2050utils.restutils import get_meta

class WorkerServer():
    def __init__(self, product_name, path, qs, cb):
        cfg = config_load(product_name)
        LOG = AppLog(cfg, service='worker')
        db = DB(cfg=cfg, log=LOG)
        mq = MQ(LOG, db, qs, cfg=cfg)
        self.cfg,self.LOG,self.db,self.mq = cfg,LOG,db,mq
        self.path,self.qs,self.cb = path,listify(qs),cb
        self.meta = None

    def run(self):
        self.loop = asyncio.get_event_loop()
        if self.db.sync_startup(loop=self.loop):
            self.LOG(4, 0, label='WORKER', label2='STARTUP', msg='DB error')
            exit(1)
        if self.mq.sync_startup(loop=self.loop):
            self.LOG(4, 0, label='WORKER', label2='STARTUP', msg='MQ error')
            exit(1)
        model = oget(self.cfg, ['app','model'])
        if model is not None:
            self.meta = self.loop.run_until_complete(get_meta(self.path, self.db, model))
        self.LOG(2, 0, label='WORKER', label2='RUN', msg='OK')
        err = self.loop.run_until_complete(self.mq.consumer(self, self.qs[0], self.cb))
        if err:
            self.LOG(4, 0, label='WORKER', label2='EXCEPTION', msg='Exit')
            sys.exit(1)

    def job_start(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_start(*args,**kwargs))
    def update_eta(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_update_eta(*args,**kwargs))
    def job_done(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_done(*args,**kwargs))
    def job_notify(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_notify(*args,**kwargs))
    def job_deliver(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_deliver(*args,**kwargs))
    def job_result(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_result(*args,**kwargs))
    def job_error(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.job_error(*args,**kwargs))
    def get_pending_jobs(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.get_pending_jobs(*args,**kwargs))
    def get_job(self,*args,**kwargs): return self.loop.run_until_complete(self.mq.get_job(*args,**kwargs))
