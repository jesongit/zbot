import logging
import sqlite3


conn = sqlite3.connect('res/gacha.db')

# 用字典返回结果
conn.row_factory = lambda cursor, row: dict([(col[0], row[idx]) for idx, col in enumerate(cursor.description)])


def query(sql):
    cursor = conn.cursor()
    try:
        logging.info(f"query sql {sql}")
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        logging.exception(e)
        return None
    finally:
        cursor.close()


def exec_sql(sql):
    cursor = conn.cursor()
    try:
        logging.info(f"exec sql {sql}")
        cursor.executescript(sql)
        conn.commit()
    except Exception as e:
        logging.exception(e)
        return None
    finally:
        cursor.close()


def exec_script(sql):
    cursor = conn.cursor()
    try:
        logging.info(f"exec script {sql}")
        cursor.executescript(sql)
        conn.commit()
    except Exception as e:
        logging.exception(e)
        return None
    finally:
        cursor.close()


def sencode(str):
    str = str.replace("'", "''")
    return str


def insert(tab, **kwargs):
    cursor = conn.cursor()
    fields, values = parse_field_value(kwargs)
    sql = f"insert into {tab} ({fields}) values ({values});"
    logging.debug(sql)
    cursor.execute(sql)
    conn.commit()


def batch_insert(tab, list, order=' or ignore'):
    place = ','.join(['?'] * len(list[0].keys()))
    list = [tuple(dict.values()) for dict in list]
    cursor = conn.cursor()
    logging.debug(f'tab: {tab} place: {place} list: {list}')
    cursor.executemany(f"insert{order} into {tab} values ({place})", list)
    conn.commit()


def delete(tab, where=None):
    cursor = conn.cursor()
    sql = f'delete from {tab}{parse_where(where)}'
    logging.debug(sql)
    cursor.execute(sql)
    conn.commit()


def select(tab, fields='*', where=None, limit=None):
    cursor = conn.cursor()
    if fields != '*':
        fields = ','.join([parse_field(field) for field in fields])
    if isinstance(limit, tuple) and len(limit) == 2:
        limit = f' limit {limit[0]},{limit[1]}'
    elif isinstance(limit, int):
        limit = f' limit {limit}'
    else:
        limit = ''
    sql = f'select {fields} from {tab}{parse_where(where)}{limit};'
    logging.debug(sql)
    cursor.execute(sql)
    return cursor.fetchall()


def update(tab, where=None, **kwargs):
    cursor = conn.cursor()
    kwargs = [f'{parse_field(key)}={parse_value(val)}' for key, val in kwargs.items()]
    up = f' set {",".join(kwargs)}'
    sql = f'update {tab}{up}{parse_where(where)}'
    logging.debug(sql)
    cursor.execute(sql)
    conn.commit()


def replace(tab, **kwargs):
    cursor = conn.cursor()
    fields, values = parse_field_value(kwargs)
    sql = f"replace into {tab} ({fields}) values ({values});"
    logging.debug(sql)
    cursor.execute(sql)
    conn.commit()


def parse_where(cond):
    if isinstance(cond, str):
        return cond
    if cond is None:
        return ''
    where, boolean = ' where', True
    for tup in cond:
        prefix = ' and ' if not boolean else ' '
        if tup == 'and' or tup == 'or':
            # 连接
            where += f' {tup}'
            boolean = True
        elif len(tup) == 2:
            # (key, val)
            where += prefix + f'{parse_field(tup[0])}={parse_value(tup[1])}'
            boolean = False
        elif tup[1] == 'in' or tup[1] == 'not in':
            # key in (1,2,3)
            if tup[2]:
                val = '(' + ','.join([parse_value(v) for v in tup[2]]) + ')'
                where += prefix + f'{parse_field(tup[0])} {tup[1]} {val}'
            boolean = False
        else:
            # key xx val
            where += prefix + f'{parse_field(tup[0])} {tup[1]} {parse_value(tup[2])}'
            boolean = False
    return where


def parse_field_value(kwargs, seq=','):
    fields = [parse_field(field) for field in kwargs.keys()]
    values = [parse_value(value) for value in kwargs.values()]
    return seq.join(fields), seq.join(values)


def parse_field(field):
    return f'`{field}`'


def parse_value(value):
    if type(value) == int:
        return str(value)
    elif value == 'null':
        return value
    elif type(value) == str:
        return f'\'{sencode(value)}\''
    else:
        return f'\'{value}\''


if __name__ == '__main__':
    pass
