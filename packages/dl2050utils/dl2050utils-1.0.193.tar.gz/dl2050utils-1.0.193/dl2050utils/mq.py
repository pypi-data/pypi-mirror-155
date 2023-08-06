import time
from datetime import datetime
import json
from aio_pika import connect_robust, Message, DeliveryMode
from dl2050utils.core import oget, listify

JOB_CREATE = 0
JOB_START = 1
JOB_DONE = 2
JOB_NOTIFY = 3
JOB_DELIVER = 4
JOB_ERROR = 99

class MQ():
    def __init__(self, log, db, qnames, cfg=None):
        self.LOG,self.db,self.qnames = log,db,listify(qnames)
        user = oget(cfg, ['mq','user'], 'admin')
        passwd = oget(cfg, ['mq','passwd'], 'password')
        self.url = f'amqp://{user}:{passwd}@mq:5672/'

    async def startup(self, loop=None):
        try:
            self.con = await connect_robust(self.url, loop=loop)
            self.ch = await self.con.channel()
            for qname in self.qnames:
                await self.ch.declare_queue(qname, durable=True, auto_delete=False)
        except Exception as e:
            self.LOG(4, 0, label='MQ', label2='connect', msg=str(e))
            return True
        self.LOG(2, 0, label='MQ', label2='STARTUP', msg='OK')
        return False

    def sync_startup(self, loop=None):
        return loop.run_until_complete(self.startup(loop=loop))
    
    async def consumer(self, w, qname, cb):
        if qname not in self.qnames:
            self.LOG(4, 0, label='MQ', label2='EXCEPTION', msg=f'Invalid qname {qname}')
            raise f'Invalid qname {qname}'
        q = await self.ch.declare_queue(qname, durable=True, auto_delete=False)
        async with q.iterator() as it:
            async for msg in it:
                async with msg.process():
                    await self.process_msg(w, msg, cb)

    async def process_msg(self, w, msg, cb):
        t0 = time.time()
        payload = json.loads(msg.body.decode())
        uid,jid = payload['uid'],payload['jid']
        self.LOG(2, 0, label='MQ', label2=f'JOB SCHEDULED', msg={'uid':uid, 'jid':jid})
        try:
            err = cb(w, jid, payload)
        except Exception as exc:
                self.LOG(4, time.time()-t0, label='MQ', label2=f'JOB EXCEPTION', msg={'uid':uid, 'jid':jid, 'exception':str(exc)})
                await self.job_error(jid)
                return
        if err:
            await self.mq.job_error(jid)
            self.LOG(4, time.time()-t0, label='MQ', label2=f'JOB ERROR', msg={'uid':uid ,'jid':jid})
            self.job_error(jid)
            return
        await self.job_done(jid)
        # msg.ch.basic_ack(delivery_tag = msg.method.delivery_tag)
        self.LOG(2, time.time()-t0, label='MQ', label2=f'JOB EXECUTED', msg={'uid':uid, 'jid':jid})

    async def publish(self, qname, uid, payload):
        job = {'uid':uid, 'payload':payload, 'jstatus':JOB_CREATE, 'eta':0, 'ts_create':datetime.now()}
        jid = await self.db.insert('jobs', job, return_key='jid')
        if jid is None:
            return None
        try:
            payload['uid'],payload['jid'] = uid,jid
            msg = Message(body=json.dumps(payload).encode(), delivery_mode=DeliveryMode.PERSISTENT)
            await self.ch.default_exchange.publish(msg, routing_key=qname)
        except Exception as e:
            self.LOG(4, 0, label='MQ', label2='publish', msg=str(e))
            return None
        return jid
        
    async def job_update(self, jid, status=None, eta=None, result=None):
        job = {'jid': jid}
        if status is not None:
            job['jstatus'] = status
            if status==JOB_START: job['ts_start'] = datetime.now()
            if status==JOB_DONE: job['ts_done'] = datetime.now()
        if eta is not None: job['eta']=eta
        if result is not None: job['result']=result
        self.LOG(1, 0, label='MQ', label2='job_update', msg=job)
        res = await self.db.update('jobs', 'jid', job)
        if res is None or res==0: return True
        return False

    async def job_start(self, jid, eta=None): return await self.job_update(jid, status=JOB_START, eta=eta)
    async def job_update_eta(self, jid, eta): return await self.job_update(jid, eta=eta)
    async def job_done(self, jid): return await self.job_update(jid, status=JOB_DONE)
    async def job_notify(self, jid): return await self.job_update(jid, status=JOB_NOTIFY)
    async def job_deliver(self, jid): return await self.job_update(jid, status=JOB_DELIVER)
    async def job_result(self, jid, result): return await self.job_update(jid, result=result)
    async def job_error(self, jid): return await self.job_update(jid, status=JOB_ERROR, eta=0)
    async def get_jobs(self, d): return await self.db.select('jobs', d)
    async def get_pending_jobs(self, uid): return await self.db.select('jobs', {'uid':uid,'jstatus':1})
    async def get_job(self, jid): return await self.db.select_one('jobs', {'jid':jid})
