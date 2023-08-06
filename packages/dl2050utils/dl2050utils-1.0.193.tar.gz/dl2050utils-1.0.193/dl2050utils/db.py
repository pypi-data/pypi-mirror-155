import asyncio
import asyncpg
import datetime
import json
from dl2050utils.core import *
from dl2050utils.log import BaseLog

def run_sql_file(db, path):
    with open(path, 'r') as f: Q_CREATE=f.readlines()
    cmds = ' '.join(Q_CREATE).split(';')
    for q in cmds:
        if len(q)<10: continue
        db.sync_execute(q+';')

def run_slq_cmds(db, q):
    for q in q.split(';'):
        if len(q)<10: continue
        db.sync_execute(q+';')

def db_insert_df(db, tbl, df, dmap=None):
    if dmap is None:
        dmap={c:c for c in df.columns}
    else:
        df = df.rename(columns=dmap)
    cols = [dmap[c] for c in dmap]
    df = df[cols]
    for i in range(len(df)):
        row = df.iloc[i]
        d = {c:row[c] for c in cols}
        if db.sync_insert(tbl, d):
            print('DB insert error')
    return False

async def calc_query_rows(con, q):
    # db.sync_select('pg_class', cols=['reltuples'], filters={'relname': 'diagsg'})
    res = await con.fetchrow(f'explain(format json) {q}')
    if res is None:
        return None
    res = json.loads(res['QUERY PLAN'])
    if res is None or not len(res):
        return None
    return oget(res[0],['Plan','Plan Rows'])

def fix_types(d):
    for k in d.keys():
        if isinstance(d[k], str): d[k]=d[k].strip()
        if isinstance(d[k], datetime.date):
            d[k] = d[k] if isinstance(d[k], datetime.datetime) else d[k].strftime("%Y-%m-%d")
    return d

def strip(e):
    if type(e)!=str: return e
    e = e.replace('\'', '')
    e.replace('\"', '')
    e.replace('\n', ' ')
    return e

def get_repr(e):
    if e is None: return 'NULL'
    if type(e)==list:
        items = [f'"{str(e1)}"' for e1 in e]
        return f"'{{{' ,'.join(items)}}}'"
    if type(e)==dict: return f"'{json.dumps(e)}'"
    if type(e)==str or type(e)==datetime.datetime: return f"'{strip(e)}'"
    return f"{e}"

def parse_filters(fs):
    if fs is None: return []
    if type(fs)!=dict and type(fs)!=list: return []
    if type(fs)==list: return [e for e in fs if type(e)==dict and 'col' in e and 'val' in e]
    return [{'col':e, 'val':fs[e]} for e in fs]

class DB():
    def __init__(self, cfg=None, log=None, dbname=None):
        if cfg is None: cfg={'db':{'host':'db','port':5432,'user':'postgres','passwd':'rootroot','dbname':'postgres'}}
        self.cfg, self.LOG = cfg, log or BaseLog()
        host = oget(cfg, ['db','host'], 'db')
        port = oget(cfg, ['db','port'], 5432)
        user = oget(cfg, ['db','user'], 'postgres')
        passwd = oget(cfg, ['db','passwd'], 'rootroot')
        if dbname is None:
            dbname = oget(cfg, ['db', 'dbname'], 'postgres')
        self.url = f'postgres://{user}:{passwd}@{host}:{port}/{dbname}'
        self.dbname = dbname

    async def startup(self, min_size=5, max_size=20, loop=None):
        try:
            self.pool = await asyncpg.create_pool(self.url, min_size=min_size, max_size=max_size, loop=loop)
        except Exception as e:
            self.LOG(4, 0, label='DBPG', label2='startup', msg=str(e))
            return True
        self.LOG(2, 0, label='DBPG', label2='startup', msg=f'CONNECTED POOL to {self.dbname}')
        return False

    def shutdown(self):
        self.pool.terminate()
        self.LOG(2, 0, label='DBPG', label2='shutdown', msg='DISCONNECTED')
        return False
    
    async def execute(self, q):
        con = await self.pool.acquire()
        try:
            res = await con.execute(q)
        except Exception as err:
            self.LOG(4, 0, label='DBPG', label2='execute', msg={'error_msg': str(err), 'query': q})
            return None
        finally:
            await self.pool.release(con)
        return res

    async def query(self, q, one=False, nrows=False, offset=None, limit=None):
        con = await self.pool.acquire()
        if q[:6].upper()!='SELECT': one=True # accounts for returning in insert
        if one: nrows=False
        try:
            if(one):
                res = await con.fetchrow(q)
                if res is None:
                    await self.pool.release(con)
                    return None
            else:
                if nrows:
                    nr = await calc_query_rows(con, q)
                    if nr is None:
                        self.LOG(4, 0, label='DB', label2='calc_query_rows', msg=q)
                        await self.pool.release(con)
                        return None
                if offset or limit: q=q[:-1]
                if offset is not None: q += f" OFFSET {offset}"
                if limit is not None: q += f" LIMIT {limit}"
                res = await con.fetch(q)
        except Exception as e:
            self.LOG(4, 0, label='DB', label2='query', msg=str(e))
            return None
        finally:
            await self.pool.release(con)
        if res is None:
            return None
        if(one):
            return fix_types(dict(res))
        res = [fix_types(dict(row)) for row in res[:100000]]
        if nrows:
            return {'data':res, 'nrows':nr}
        return res
    
    async def get_trows(self, tbl):
        q = f"select reltuples as nrows from pg_class where relname='{tbl}'"
        con = await self.pool.acquire()
        res = await con.fetchrow(q)
        if res is None:
            return -1
        return int(dict(res)['nrows'])

    async def select(self, tbl, filters=None, sfilters=None, cols='*', sort=None, ascending=True, offset=None, limit=None, one=False):
        if cols is not None: cols=', '.join(cols)
        offset,limit = offset or 0,limit or 32
        q = f"SELECT {cols} FROM {tbl}"
        fs,sfs = parse_filters(filters),parse_filters(sfilters)
        fs = [{**e, 'op':'='} if 'op' not in e else e for e in fs]
        if len(fs):
            fs = ' AND '.join([f"{e['col']}{e['op']}'{e['val']}'" for e in fs])
            q += f" WHERE {fs}"
        if len(sfs):
            q+=' WHERE ' if not len(fs) else ' AND '
            q += ' AND '.join([f"{e['col']} ILIKE '%{e['val']}%'" for e in sfs])
        if sort is not None: q += f" ORDER BY {sort} " + ("ASC" if ascending else "DESC")
        q += ';'
        return await self.query(q, one=one, nrows=True, offset=offset, limit=limit)

    async def select_one(self, tbl, filters):
        return await self.select(tbl, filters=filters, one=True)
    
    async def insert(self, tbl, d, return_key=None):
        q = f"INSERT INTO {tbl} ("
        for k in d.keys(): q += f"{k}, "
        q = q[:-2] + ") VALUES ("
        for k in d.keys(): q = q + get_repr(d[k]) + ', '
        q = q[:-2] + ")"
        if return_key is not None:
            q += f" returning {return_key};"
            res = await self.query(q, one=True)
            if res is not None and len(res):
                return res[return_key]
            return None
        res = await self.execute(q)
        if res=='INSERT 0 1': return False
        return True

    async def delete(self, tbl, k, v):
        if k is None or v is None: return True
        q = f"DELETE FROM {tbl} WHERE {k}='{v}'"
        res = await self.execute(q)
        if res is None: return True
        n = int(res[7:])
        if n==0: return True
        return False
    
    async def delete_all(self, tbl):
        q = f"DELETE FROM {tbl}"
        res = await self.execute(q)
        if res is None: return True
        return False

    async def update(self, tbl, ks, d):
        ks = listify(ks)
        for k in ks:
            if not k in d:
                self.LOG(4, 0, label='DBPG', label2='update', msg=f'key error: {k}')
                return True
        setvars = ', '.join([f"{k}={get_repr(d[k])}" for k in d if k not in ks+['nrows'] and d[k] is not None])
        q = f"UPDATE {tbl} SET {setvars}"
        filters = ' AND '.join([f"{k}='{d[k]}'" for k in ks if d[k] is not None])
        q += f" WHERE {filters};"
        res = await self.execute(q)
        if res is None: return True
        n = int(res[7:])
        if n==0: return True
        return False

    async def insert_rows(self, tbl, rows, delete=False):
        if delete:
            res = await self.execute(f'DELETE FROM {tbl}')
            if res is None:
                return res
        for row in rows:
            res = await self.insert(tbl, row)
            if res is None:
                return res
        return len(rows)

    def sync_startup(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.startup(*args, **kwargs))
    def sync_execute(self, q): return asyncio.get_event_loop().run_until_complete(self.execute(q))
    def sync_query(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.query(*args, **kwargs))
    def sync_select(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.select(*args, **kwargs))
    def sync_select_one(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.select_one(*args, **kwargs))
    def sync_insert(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.insert(*args, **kwargs))
    def sync_delete(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.delete(*args, **kwargs))
    def sync_delete_all(self, *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.delete_all(*args, **kwargs))
    def sync_update(self,  *args, **kwargs): return asyncio.get_event_loop().run_until_complete(self.update(*args, **kwargs))
