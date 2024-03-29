#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

from .mysql import *
GACHA_TAB = 'gacha_xqtd'
ROLE_INFO = 'role_info'

'''
{'uid': '105846671',
  'gacha_id': '4001',
  'gacha_type': '2',
  'item_id': '1101',
  'count': '1',
  'time': '2023-04-26 20:26:01',
  'name': '布洛妮娅',
  'lang': 'zh-cn',
  'item_type': '角色',
  'rank_type': '5',
  'id': '1682511000013659771'}
'''

# 卡池类型
gacha_type_list = [
    1,      # 常驻跃迁
    2,      # 新手跃迁
    11,     # 限时角色
    12,     # 限时武器
]

# 限时角色列表
limited_list = [
    name_to_id('希儿'),
    name_to_id('景元'),
    name_to_id('银狼'),

    name_to_id('于夜色中'),
    name_to_id('拂晓之前'),
    name_to_id('雨一直下'),
]


def gacha_type_name(gacha_type: int):
    if gacha_type == 1:
        return '常驻跃迁'
    elif gacha_type == 2:
        return '新手跃迁'
    elif gacha_type == 11:
        return '限时角色'
    elif gacha_type == 12:
        return '限时武器'


def insert_gacha(dict_list):
    data_list = []
    for data in dict_list:
        for k, v in data.items():
            if v.isdecimal():
                data[k] = int(v)
        data_list.append(data)
    batch_insert(GACHA_TAB, data_list, extra=' ignore')


def get_gacha_by_uid(uid):
    return select(GACHA_TAB, where=[('uid', uid)])


def is_limited(item_id):
    return item_id in limited_list


def check_gacha_id(end_id):
    return isinstance(select(GACHA_TAB, where=[('id', end_id)]), list)


def insert_role_info(uid: int, role_info: dict):
    role_id = role_info['avatarId']
    return insert_or_update(ROLE_INFO, uid=uid, role_id=role_id, info=str(role_info))
    # data = [{'uid': uid, 'role_id': role_id, 'info': json.dumps(role_info)}]
    # return batch_insert('role_info', data)


def select_role_info(uid: int, role_id):
    return select(ROLE_INFO, where=[('uid', uid), ('role_id', role_id)])


if __name__ == '__main__':
    pass
