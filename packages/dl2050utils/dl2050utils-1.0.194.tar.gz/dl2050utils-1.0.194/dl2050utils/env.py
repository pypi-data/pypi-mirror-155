import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

def find_yml(name):
    p = Path(f'./{name}')
    if p.exists(): return p
    p = Path(f'/run/secrets/{name}')
    if p.exists(): return p
    return None

def config_load(name=None):
    load_dotenv()
    name = 'config.yml' if name is None else f'config-{name}.yml'
    fname = find_yml(name)
    if fname is None:
        raise RuntimeError('Unable to find config file')
    with open(str(fname),'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            raise RuntimeError(f'Unable to load config file: {str(err)}')
    return cfg

def get_db_url(Config, with_db_name=False):
    if Config is None:
        return None
    if not 'db' in Config:
        return None
    if os.getenv('development') is None:
        if not 'host' in Config['db']:
            return None
        host = Config['db']['host']
    else:
        if not 'host_dev' in Config['db']:
            return None
        host = Config['db']['host_dev']
    if not 'port' in Config['db']:
        port = 3306
    else:
        port = Config['db']['port']
    if not 'name' in Config['db']:
        return None
    if not 'passwd' in Config['db']:
        return None
    passwd = Config['db']['passwd']
    url = f'mysql+pymysql://root:{passwd}@{host}:{port}'
    if with_db_name:
        name = Config['db']['name']
        url = f'{url}/{name}'
    return url

def get_rest_url(Config):
    if Config is None:
        return None
    if not 'rest' in Config:
        return None
    if os.getenv('development') is None:
        if not 'host' in Config['rest']:
            return None
        host = Config['rest']['host']
    else:
        if not 'host_dev' in Config['rest']:
            return None
        host = Config['rest']['host_dev']
    if not 'port' in Config['rest']:
        return None
    port = Config['rest']['port']
    url = f'{host}:{port}'
    return url