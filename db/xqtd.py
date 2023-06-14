#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .mysql import *
tab = 'gacha_xqtd'

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
limited_role_list = [
    1102,   # 希儿
    1204,   # 景元
    1006,   # 银狼
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
    batch_insert(tab, data_list, extra=' ignore')


def get_gacha_by_uid(uid):
    return select(tab, where=[('uid', uid)])


def is_limited(item_id):
    return item_id in limited_role_list


def check_gacha_id(end_id):
    return isinstance(select(tab, where=[('id', end_id)]), list)


if __name__ == '__main__':
    pass
