import db.sqlite as sqlite
from botpy import logger

tab = 'user'


def update(user_id: str, key, val):
    where = [('user_id', user_id)]
    res, = sqlite.select(tab, fields=[key], where=where),
    logger.info(f'res: {res}, {val}')
    if not res:
        kwargs = {'user_id': user_id, key: val}
        sqlite.insert(tab, **kwargs)
        return True, '绑定成功'
    elif res[0][key] == val:
        return False, '请勿重复绑定'
    else:
        sqlite.update(tab, where, **{key: val})
        return True, '更新成功'


def get_uid(user_id: str, key):
    res = sqlite.select(tab, fields=[key], where=[('user_id', user_id)])
    logger.debug(res)
    if res:
        return True, res[0][key]
    return False, None


if __name__ == '__main__':
    pass
