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


def parse_update_set(kwargs):
    kwargs = [f'{parse_field(key)}={parse_value(val)}' for key, val in kwargs.items()]
    return ','.join(kwargs)


def parse_select_fields(fields):
    if fields == '*':
        return fields
    return ','.join([parse_field(field) for field in fields])


def parse_select_limit(limit):
    if isinstance(limit, tuple) and len(limit) == 2:
        return f' limit {limit[0]},{limit[1]}'
    elif isinstance(limit, int):
        return f' limit {limit}'
    return ''


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


def sencode(str: str):
    return str.replace('\'', '\'\'').replace(r'\\', r'\\\\')
