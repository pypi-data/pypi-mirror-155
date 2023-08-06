import datetime
import random
import json
import hashlib
import jwt
from starlette.responses import JSONResponse
import orjson

class HTTPException(Exception):
    def __init__(self, status_code, detail:None):
        if detail is None: detail = ''
        self.status_code = status_code
        self.detail = detail

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"

async def db_increase(db, tbl, k, kv, c):
    try:
        row = await db.select_one(tbl, {k: kv})
        row[c] += row[c]+1
        res = await db.update(tbl, row)
        if res:
            raise HTTPException(401, detail=f'db_increase error: tbl={tbl}, k={k}, kv={kv}, c={c}')
    except Exception as err:
        raise HTTPException(401, detail=f'db_increase exception: tbl={tbl}, k={k}, kv={kv}, c={c}')

def get_required_args(payload, args):
    args2,miss = {},[]
    for e in args:
        if e not in payload or payload[e] is None:
            miss.append(e)
        else:
            args2[e] = payload[e]
    if len(miss):
        raise HTTPException(400, f'Missing required args: {", ".join(miss)}')
    return args2

def get_optional_args(payload, required, args):
    optional = {e:payload[e] for e in payload if e not in required}
    invalid = []
    for e in optional:
        if e not in args:
            invalid.append(e)
    if len(invalid):
        raise HTTPException(400, f'Invalid optional args: {", ".join(invalid)}')
    return optional

def get_required(payload, args):
    args2 = []
    for e in args:
        if e not in payload or payload[e] is None:
            raise HTTPException(400, detail=f'Missing required arg {e}')
        args2.append(payload[e])
    return args2

def check_required(LOG, label, label2, payload, args):
    miss = []
    for e in args:
        if not (e in payload) or payload[e] is None:
            miss.append(e)
    if len(miss)>1:
        rest_exception(LOG, label, label2, f"Missing required args: {', '.join(miss)}")
    if len(miss):
        rest_exception(LOG, label, label2, f"Missing required arg: {miss[0]}")

def check_all_attrs(d, attrs):
    for e in attrs:
        if not (e in d): return True
    return False

class OrjsonResponse(JSONResponse):
    def render(self, content):
        return orjson.dumps(content)

def mk_key(n=4):
    return ''.join([chr(48+i) if i<10 else chr(65-10+i) for i in [random.randint(0, 26+10-1) for _ in range(n)]])
    # return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def get_hash(o, secret):
    o1 = {**o}
    o1['secret']=secret
    return hashlib.sha224(json.dumps(o1).encode()).hexdigest()

def check_hash(o, h, secret):
    o1 = {**o}
    o1['secret']=secret
    return get_hash(o1, secret)==h

def mk_jwt_token(uid, email, secret):
    JWT_EXP_DELTA_SECONDS = 30*24*3600
    payload = { 'uid': uid, 'email': email, 'username': '', 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)}
    return jwt.encode(payload, secret, 'HS256') # .decode('utf-8')

def rest_ok(result):
    return OrjsonResponse({'status': 'OK', 'result': result})

def rest_error(LOG, label, label2, error_msg):
    LOG(4, 0, label=label, label2=label2, msg=error_msg)
    return OrjsonResponse({'status': 'ERROR', 'error_msg': error_msg})

def rest_exception(LOG, label, label2, msg):
    LOG(4, 0, label=label, label2=label2, msg=msg)
    raise HTTPException(400, f'EXCEPTION: {msg}')

async def get_meta(db, model):
    row = await db.select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None

def sync_get_meta(db, model):
    row = db.sync_select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None

def mk_weeks(ds1='2018-01-01', ds2=None, weekday=6):
    d1 = datetime.datetime.strptime(ds1, '%Y-%m-%d').date()
    delta = 5 - d1.weekday()
    if delta<0: delta+=7
    d1 += datetime.timedelta(days=delta)
    d2 = datetime.datetime.now().date() if ds2 is None else datetime.datetime.strptime(ds2, '%Y-%m-%d').date()
    ds = [d.strftime("%Y-%m-%d") for d in rrule.rrule(rrule.WEEKLY, dtstart=d1, until=d2)]
    return ds[::-1]

def get_week2(weeks, week): return weeks[weeks.index(week)+1] if weeks.index(week)+1<len(weeks) else None

def s3_urls(s3, bucket_name, prefix):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1024)['Contents']
    return [f'http://{bucket_name}.s3-eu-west-1.amazonaws.com/{e["Key"]}' for e in response]
