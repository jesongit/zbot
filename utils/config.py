import yaml
from pathlib import Path
from pymysql import cursors

config = yaml.safe_load(Path('config.yaml').open(encoding='utf8'))


def appid():
    return config['appid']


def token():
    return config['token']


def log_level():
    return config['log_level']


def test_channel():
    return config['test_channel']


def mysql_config():
    return {
        'host': config['mysql_host'],
        'port': config['mysql_port'],
        'user': config['mysql_user'],
        'password': config['mysql_password'],
        'database': config['mysql_database'],
        'cursorclass': cursors.DictCursor
    }
