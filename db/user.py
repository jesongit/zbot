#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .mysql import *
from botpy import logger

tab = 'user'


def update_key_val(user_id: str, key, val):
    flag, my_val = get_uid(user_id, key)

    user_id = int(user_id)
    logger.info(f'{flag}: {val}, {my_val}')
    if not flag:
        kwargs = {'user_id': user_id, key: val}
        if insert(tab, **kwargs):
            return True, '绑定成功'
        return False, '绑定失败'
    elif my_val == val:
        return False, '请勿重复绑定'
    else:
        if update(tab, where=[('user_id', user_id)], **{key: val}):
            return True, '更新成功'
        return False, '更新失败'


def get_uid(user_id: str, key):
    user_id = int(user_id)
    res = select(tab, fields=[key], where=[('user_id', user_id)])
    logger.debug(f'user_id: {user_id} key: {res}')
    if res:
        return True, res[0][key]
    return False, None


if __name__ == '__main__':
    pass
