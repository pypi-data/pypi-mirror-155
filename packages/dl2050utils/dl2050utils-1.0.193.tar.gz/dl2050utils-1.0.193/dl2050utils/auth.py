from datetime import datetime, timezone
import bcrypt
from starlette.routing import Route
from dl2050utils.core import oget
from dl2050utils.com import send_otp
from dl2050utils.restutils import HTTPException, get_required, rest_ok, rest_error, mk_key, mk_jwt_token

NOT_REGISTERED = 0
WAIT_SET_PASSWD = 1
SUSPENDED = 2
SUSPENDED_LICENCE = 3
SUSPENDED_FAILS = 4
SUSPENDED_REQUESTS = 5
ACTIVE = 10

AUTHORIZED = 100
NOT_AUTHORIZED = 101
WRONG_PASSWD = 102
REGISTER_NOT_ALLOWED = 103
OTP_ERROR = 104
OTP_EXPIRED = 105
PASSWORD_CHANGED = 106

MAX_FAILS = 3
MAX_REQUESTS = 1e4

async def db_update(db, tbl, kc, d, prefix=''):
    res = await db.update(tbl, kc, d)
    if res:
        raise HTTPException(401, detail=f'{prefix+": " if prefix else ""}update_user db error')

def increase(d, f):
    if d is None or f not in d: return d
    if d[f] is None: d[f]=0
    d[f] += 1
    d['ts_access'] = datetime.now(timezone.utc)
    if f=='logins': d['ts_login'],d['fails'] = datetime.now(timezone.utc),0
    return d

class Auth():
    def __init__(self, cfg, LOG, NOTIFY, db):
        self.cfg, self.LOG, self.NOTIFY, self.db = cfg, LOG, NOTIFY, db

    def get_routes(self):
        return [
            Route('/api/auth/auth_info', endpoint=self.auth_info, methods=['GET']),
            Route('/api/auth/check_user', endpoint=self.check_user, methods=['POST']),
            Route('/api/auth/login', endpoint=self.login, methods=['POST']),
            Route('/api/auth/register', endpoint=self.register, methods=['POST']),
            Route('/api/auth/set_passwd', endpoint=self.set_passwd, methods=['POST']),
            Route('/api/auth/recover_passwd', endpoint=self.recover_passwd, methods=['POST']),
            Route('/api/auth/change_passwd', endpoint=self.change_passwd, methods=['POST']),
        ]

    async def startup(self):
        try:
            self.product = self.cfg['app']['product']
            self.auth_secret = self.cfg['rest']['auth_secret']
            self.allow_register = oget(self.cfg, ['rest', 'allow_register'], False)
            self.strong_passwd = oget(self.cfg, ['rest', 'strong_passwd'], False)
            self.otp_timeout = oget(self.cfg, ['rest', 'otp_timeout'], False)
            self.otp_mode = oget(self.cfg, ['rest', 'otp_mode'], False)
        except Exception as e:
            self.LOG(4, 0, label='AUTH', label2='startup', msg={'error_msg': str(e)})
            return True
        self.LOG(2, 0, label='AUTH', label2='startup', msg=f'OK')
        return False   

    async def shutdown(self):
        self.LOG(2, 0, label='AUTH', label2='shutdown', msg='OK')
        return False

    async def register_requests(self, url, uid, t, error):
        await self.db.insert('metrics', {'ts': datetime.now(timezone.utc), 'uid':uid, 'url':url, 't':t, 'error':error})
        if uid==-1: return
        user = await self.db.select_one('users', {'id': uid})
        user = increase(user, 'requests')
        if user['requests'] > MAX_REQUESTS: user['ustatus'] = SUSPENDED_REQUESTS
        await db_update(self.db, 'users', 'email', user)

    async def gen_otp(self, user, return_code=WAIT_SET_PASSWD):
        if self.otp_mode=='phone' and user['phone'] is None:
            return rest_error(self.LOG, 'AUTH', 'register', 'phone not defined')
        otp = mk_key(n=4)
        self.LOG(2, 0, label='GEN_OTP', label2='New OTP', msg={'email': user['email'], 'OTP': otp})
        err = send_otp(self.NOTIFY, self.otp_mode, self.product, user['email'], user['phone'], otp)
        if err is not None:
            self.LOG(4, 0, label='AUTH', label2='gen_otp', msg=err)
            return rest_error(self.LOG, 'AUTH', 'register', 'send key by email error')
        user['otp'],user['ts_passwd'],user['ustatus'] =  otp, datetime.now(timezone.utc),WAIT_SET_PASSWD
        await db_update(self.db, 'users', 'email', user, prefix='gen_otp')
        return rest_ok({'user_status': return_code})

    async def check_auth(self, request):
        uid = request.user.display_name
        user = await self.db.select_one('users', {'id': uid})
        if user is None:
            msg = 'invalid user'
            self.LOG(4, 0, label='AUTH', label2='check_auth', msg={'uid':uid, 'exception':msg})
            raise HTTPException(401, detail=msg)
        if user['ustatus']!=ACTIVE:
            msg = 'user not active'
            self.LOG(4, 0, label='AUTH', label2='check_auth', msg={'uid':uid, 'exception':msg})
            raise Exception('Authorization error: user not active')
        return {'uid':uid, 'email':user['email'], 'status':user['ustatus'], 'org':user['org'], 'dep':user['dep']}

    async def auth_info(self, request):
        return rest_ok({'allow_register': self.allow_register, 'strong_passwd': self.strong_passwd, 'otp_timeout': self.otp_timeout,
                        'otp_mode': self.otp_mode})

    async def check_user(self, request):
        data = await request.json()
        [email] = get_required(data,['email'])
        user = await self.db.select_one('users', {'email':email})
        if user is None:
            return rest_ok({'user_status': NOT_REGISTERED})
        if not self.allow_register and user['ustatus']==NOT_REGISTERED:
            return await self.gen_otp(user, WAIT_SET_PASSWD)
        if user['ustatus']==ACTIVE:
            user = increase(user, 'logins')
            await db_update(self.db, 'users', 'email', user)
            return rest_ok({'user_status': user['ustatus']})
        return rest_ok({'user_status':user['ustatus']})

    async def login(self, request):
        uid = request.user.display_name
        data = await request.json()
        [email,passwd] = get_required(data,['email', 'passwd'])
        user = await self.db.select_one('users', {'email':email})
        if user is None:
            self.LOG(3, 0, label='AUTH', label2='login', msg={'user':email, 'error_message':'user not registered'})
            return rest_ok({'user_status': NOT_REGISTERED})
        if user['ustatus'] in [NOT_REGISTERED, WAIT_SET_PASSWD, SUSPENDED, SUSPENDED_LICENCE]:
            self.LOG(3, 0, label='AUTH', label2='login', msg={'user':email, 'error_message': 'user not active'})
            return rest_ok({'user_status': user['ustatus']})
        if not "passwd" in user or user['passwd'] is None or passwd is None:
            return rest_error(self.LOG, 'AUTH', 'login', 'no passwd provided')
        if not bcrypt.checkpw(passwd.encode(), user['passwd'].encode()):
            user = increase(user, 'fails')
            if user['fails'] > MAX_FAILS: user['ustatus'],user['fails'] = SUSPENDED_FAILS,0
            await db_update(self.db, 'users', 'email', user)
            if user['fails'] > MAX_FAILS:
                self.LOG(4, 0, label='AUTH', label2='login', msg={'user':email, 'error_message':'user suspend - too many login fails'})
                return rest_ok({'user_status': SUSPENDED_FAILS})
            else:
                self.LOG(3, 0, label='AUTH', label2='login', msg={'user': email, 'error_message': 'wrong password'})
                return rest_ok({'user_status': WRONG_PASSWD})
        jwt_token = mk_jwt_token(user['id'], email, self.auth_secret)
        user = increase(user, 'logins')
        await db_update(self.db, 'users', 'email', user)
        return rest_ok({'user_status':AUTHORIZED, 'jwt_token':jwt_token,
                        'user_info':{'uid':uid, 'role':user['role'], 'org':user['org'], 'dep':user['org']}})

    async def register(self, request):
        data = await request.json()
        [email] = get_required(data,['email'])
        user = await self.db.select_one('users', {'email':email})
        if user is None:
            if not self.allow_register:
                return rest_ok({'user_status': REGISTER_NOT_ALLOWED})
            user = {'email':email, 'ustatus':NOT_REGISTERED, 'ts_insert':datetime.now(timezone.utc),
                    'logins':0, 'fails':0, 'requests':0}
            await self.db.insert('users', user)
        if user['ustatus'] in [ACTIVE, SUSPENDED, SUSPENDED_LICENCE, WAIT_SET_PASSWD]:
            return rest_ok({'user_status': user['ustatus']})
        user['ustatus'] = WAIT_SET_PASSWD
        await db_update(self.db, 'users', 'email', user)
        return await self.gen_otp(user, WAIT_SET_PASSWD)

    async def recover_passwd(self, request):
        data = await request.json()
        [email] = get_required(data,['email'])
        user = await self.db.select_one('users', {'email':email})
        if user is None:
            return rest_error(self.LOG, 'AUTH', 'SERVICE_ERROR', 'recover_passwd: user not found')
        user['ustatus'] = WAIT_SET_PASSWD
        await db_update(self.db, 'users', 'email', user)
        await self.gen_otp(user, WAIT_SET_PASSWD)
        return rest_ok({})

    async def set_passwd(self, request):
        data = await request.json()
        [otp,passwd] = get_required(data,['otp','passwd'])
        user = await self.db.select_one('users', {'otp': otp})
        if user is None:
            return rest_ok({'user_status': OTP_ERROR})
        delta = int(datetime.now(timezone.utc).strftime("%s")) - int(user['ts_passwd'].strftime("%s"))
        if delta > self.otp_timeout:
            self.LOG(3, 0, label='AUTH', label2='OTP', msg=f'OTP expiered - delta={delta}')
            return await self.gen_otp(user, OTP_EXPIRED)
        hashed = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
        user['passwd'],user['ts_passwd'],user['otp'],user['ustatus'] = hashed.decode(),datetime.now(timezone.utc),'',ACTIVE
        increase(user, 'logins')
        await db_update(self.db, 'users', 'email', user)
        jwt_token = mk_jwt_token(user['id'], user['email'], self.auth_secret)
        return rest_ok({'user_status': AUTHORIZED, 'jwt_token': jwt_token})

    async def change_passwd(self, request):
        uid = request.user.display_name
        if uid is None or uid=='':
            return rest_error(self.LOG, 'AUTH', 'change_passwd', 'User ID not set')
        user = await self.db.select_one('users', {'id': uid})
        if user is None:
            return rest_error(self.LOG, 'AUTH', 'SERVICE_ERROR', 'change_passwd: user not registered')
        data = await request.json()
        [passwd,new_passwd] = get_required(data,['passwd','new_passwd'])
        if not "passwd" in user or user['passwd'] is None or passwd is None:
            return rest_error(self.LOG, 'AUTH', 'SERVICE_ERROR', 'change_passwd: password error')
        if not bcrypt.checkpw(passwd.encode(), user['passwd'].encode()):
            return rest_ok({'user_status': WRONG_PASSWD})
        hashed = bcrypt.hashpw(new_passwd.encode(), bcrypt.gensalt())
        user['passwd'],user['otp'],user['ustatus'] = hashed.decode(),'',ACTIVE
        await db_update(self.db, 'users', 'email', user)
        return rest_ok({'user_status': PASSWORD_CHANGED})
