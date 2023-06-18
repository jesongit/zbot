#!/usr/bin/python
# -*- coding: UTF-8 -*-
from queue import Queue
from pymysql import connect

from .make_sql import *
from utils import *


def new_connect():
    return connect(**mysql_config())


def init_pool(cnt=3):
    queue = Queue()
    for i in range(cnt):
        queue.put(new_connect())
    return queue


pool = init_pool()


def clear_pool():
    while pool.qsize():
        conn = pool.get()
        conn.close()


def query(sql, args=None):
    conn = pool.get()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, args=args)
        res = cursor.fetchall()
        cursor.close()
        return res
    except Exception as e:
        cursor.close()
        return None
    finally:
        pool.put(conn)


def execute(sql, args=None):
    conn = pool.get()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, args)
        cursor.close()
        conn.commit()
        return True
    except Exception as e:
        cursor.close()
        return False
    finally:
        pool.put(conn)


def executemany(sql, args=None):
    conn = pool.get()
    cursor = conn.cursor()
    try:
        assert isinstance(args, list) and len(args) > 0
        cursor.executemany(sql, args)
        cursor.close()
        conn.commit()
        return True
    except Exception as e:
        cursor.close()
        return False
    finally:
        pool.put(conn)


def get_extra(kwargs):
    if 'extra' in kwargs:
        extra = kwargs['extra']
        del kwargs['extra']
        return extra, kwargs
    return '', kwargs


def make_fill_values(key_num):
    return ','.join(['%s']*key_num)


def insert(tab, **kwargs):
    extra, kwargs = get_extra(kwargs)
    fields, values = parse_field_value(kwargs)
    return execute(f'insert{extra} into {tab} ({fields}) values ({values});')


def batch_insert(tab, values, **kwargs):
    extra, kwargs = get_extra(kwargs)
    fields, _ = parse_field_value(values[0])
    filler = make_fill_values(len(values[0].keys()))

    sql = f'insert{extra} into {tab} ({fields}) values ({filler})'
    return executemany(sql, [tuple(data.values()) for data in values])


def delete(tab, where=None):
    return execute(f'delete from {tab}{parse_where(where)};')


def update(tab, where=None, **kwargs):
    return execute(f'update {tab} set {parse_update_set(kwargs)}{parse_where(where)};')


def select(tab, fields='*', where=None, limit=None):
    return query(f'select {parse_select_fields(fields)} from {tab}{parse_where(where)}{parse_select_limit(limit)};')


if __name__ == '__main__':
    pass
