#!/usr/bin/python
# -*- coding: UTF-8 -*-
import yaml
from botpy import logger
from pathlib import Path
from pymysql import cursors

config = yaml.safe_load(Path('config.yaml').open(encoding='utf8'))
name2id = yaml.safe_load(Path('name.yaml').open(encoding='utf8'))


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

        'charset': 'utf8mb4',
        'cursorclass': cursors.DictCursor,
    }


def name_to_id(name):
    if name in name2id:
        return name2id[name]
    return 0
