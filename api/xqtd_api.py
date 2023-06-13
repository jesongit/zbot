import json
import time
import requests
import urllib.parse
from pathlib import Path

from db import *

'''
ret_data = {
    'retcode': 0,
    'message': 'OK',
    'data': {
        'page': '1',
        'size': '20',
        'list': [{'uid': '105846671',
                  'gacha_id': '1001',
                  'gacha_type': '1',
                  'item_id': '20010',
                  'count': '1',
                  'time': '2023-06-09 00:47:38',
                  'name': '戍御',
                  'lang': 'zh-cn',
                  'item_type': '光锥',
                  'rank_type': '3',
                  'id': '1686240600002162071'}],
        'region': 'prod_gf_cn', 'region_time_zone': 8}}
'''

GACHA_URL = 'https://api-takumi.mihoyo.com/common/gacha_record/api/getGachaLog'


def page_gacha_record(authkey, type, page, end_id, game_biz):
    try:
        params = {'authkey_ver': 1, 'authkey': authkey,
                  'lang': 'zh-cn', 'size': 20, 'end_id': end_id,
                  'page': page, 'gacha_type': type, 'game_biz': game_biz}
        req = requests.get(GACHA_URL, params=params)
        assert req.status_code == 200, f'请求错误 code: {req.status_code}'
        data = req.json()
        logger.debug(f'code: {req.status_code} text: {req.text}')
        assert data['retcode'] == 0, f'text: {req.text}'
        if not data['data']['list']:
            return True, 0, []
        return True, data['data']['list'][-1]['id'], data['data']['list']
    except Exception as e:
        logger.exception(e)
        return False, 0, []


def get_gache_record(authkey, game_biz, type):
    stop, res, page, end_id = False, [], 1, 0
    while not stop:
        flag, end_id, ret = page_gacha_record(authkey, type, page, end_id, game_biz)
        if not flag:
            return []
        stop, page, res = len(ret) < 20 or check_gacha_id(end_id), page + 1, res + ret
        time.sleep(3)
    # Path(f'./xqtd_{type}.json').write_text(str(res).replace('\'', '"'), encoding='utf8')
    return res


def load_all_gache_record(authkey, game_biz):
    for type in gacha_type_list:
        file = Path(f'xqtd_{type}.json')
        if file.exists():
            ret = json.loads(file.read_text(encoding='utf8'))
        else:
            ret = get_gache_record(authkey, game_biz, type)
        logger.info(f'type: {type} num: {len(ret)}')
        logger.debug(f'record: {ret}')
        if ret:
            xqtd.insert_gacha(ret)


def parse_web_url(url: str):
    try:
        if not url.startswith(GACHA_URL):
            return False, None, None
        # url = urllib.parse.unquote(url)
        url = urllib.parse.urlparse(url.replace('&amp;', '&'))
        params = urllib.parse.parse_qs(url.query)
        logger.debug(f'url: {url} params: {params}')
        return True, params['authkey'][0], params['game_biz'][0]
    except Exception as e:
        logger.exception(e)
        return False, None, None


def gen_gacha_img(uid):
    # rank_type, pool_type = get_gacha_by_uid(uid)
    # source = pd.DataFrame({'品质': rank_type, '卡池': pool_type})
    # base = alt.Chart(source).encode(
    #     theta=alt.Theta("count(卡池):Q").stack(True),
    #     color=alt.Color("品质:N").legend(None),
    # )
    #
    # pie = base.mark_arc(outerRadius=120)
    # text = base.mark_text(radius=140, size=20).encode(
    #     text="品质:N"
    # )
    #
    # im = io.BytesIO()
    # (pie + text).save(im, format='png')
    # alt.Chart(source, title='抽卡分析').mark_bar().encode(
    #     x='品质:N', y='count(卡池):Q', color='卡池:N'
    # ).save(im, format='png')
    return None


# def gen_pool_img(type, rtype):
#     if len(rtype) == 0:
#         return None
#     source = pd.DataFrame({'品质': rtype.keys(), '数量': rtype.values()})
#     im = io.BytesIO()
#     alt.Chart(source, width=100, height=200, title=name(type)).mark_bar().encode(
#         x='品质:N', y='数量:Q', color='品质:N'
#     ).save(im, format='png')
#     return Image.open(im)


def gen_gacha_info(uid):
    res = get_gacha_by_uid(uid)
    if not res:
        return False, None
        return '请先导入抽卡记录\n1. 回复"/help"查看获取抽卡链接教程.\n2. "/url 抽卡链接" 导入抽卡记录'
    return True, '\n' + '\n'.join([gen_gacha_str(gacha_type, res) for gacha_type in gacha_type_list])


def gen_gacha_str(gacha_type, data_list):
    data_list = [data for data in data_list if data['gacha_type'] == gacha_type]
    pool_name = gacha_type_name(gacha_type)
    data_list.sort(key=lambda data: data['time'])
    stat, record = {}, []
    for index, data in enumerate(data_list):
        rank_type = data['rank_type']
        val = 0 if rank_type not in stat else stat[rank_type]
        stat[rank_type] = val + 1

        if rank_type == 5:
            record.append((index + 1, data))
    total = len(data_list)
    bd_str = gen_bd_str(gacha_type, record, total)
    if stat:
        stat = ' | '.join([f'{rank_type}星: {num} 个' for rank_type, num in sorted(list(stat.items()))]) + '\n'
    else:
        stat = ''
    if record:
        record = ''.join([f'{data["time"]}: [{count}] {data["name"]}\n' for count, data in record])
    else:
        record = ''
    return f'{pool_name}: \n{stat}{bd_str}{record}'


def gen_bd_str(gacha_type, record, total):
    rem1, rem2 = total % 90, total % 180
    if gacha_type == 1:
        # 常驻
        bd, bd_type = 90 - rem1, ''
    elif gacha_type == 2:
        if record:
            return ''
        # 新手
        bd, bd_type = 50 - total, ''
    elif record:
        # 抽到过5x 并且是限定
        bd, bd_type = 90 - rem1, '小' if is_limited(record[-1][1]['item_id']) else '大'
    else:
        bd, bd_type = 90 - rem1, '小'
    return f'已抽{total}次，还差 {bd} 抽触发{bd_type}保底\n'


if __name__ == '__main__':
    pass
