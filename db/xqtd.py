import db.sqlite as sqlite

tab = 'xqtd'

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

uid             int
gacha_id        int
gacha_type      int
item_id         int
name            text
time            text
id              text
rank_type       int
'''

gacha_type_list = [
    1,      # 常驻跃迁
    2,      # 新手跃迁
    11,     # 限时角色
    12,     # 限时武器
]

role_list = [1102, 1204, 1006]  # 限时角色列表


def gacha_type_name(gacha_type: int):
    if gacha_type == 1:
        return '常驻跃迁'
    elif gacha_type == 2:
        return '新手跃迁'
    elif gacha_type == 11:
        return '限时角色'
    elif gacha_type == 12:
        return '限时武器'


def insert(list):
    list = [{
        'id': dict['id'],
        'name': dict['name'],
        'time': dict['time'],
        'rank_type': int(dict['rank_type']),
        'uid': int(dict['uid']),
        'gacha_id': int(dict['gacha_id']),
        'gacha_type': int(dict['gacha_type']),
        'item_id': int(dict['item_id']),
    } for dict in list]
    sqlite.batch_insert(tab, list)


def get_gacha_by_uid(uid):
    # rank_type, pool_type = [], []
    # for data in sqlite.select(tab, where=[('uid', uid)]):
    #     print(data)
    #     rank_type.append(str(data['rank_type']) + '星')
    #     pool_type.append(gacha_type_name(data['gacha_type']))
    return sqlite.select(tab, where=[('uid', uid)])


def is_limited(item_id):
    return item_id in role_list


if __name__ == '__main__':
    pass
