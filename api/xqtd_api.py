import time
import requests
import urllib.parse

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
    xqtd_uid = 0
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
            xqtd_uid = ret[0]['uid']
    return int(xqtd_uid)


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
    remain = total if not record else total - record[-1][0]
    rem1, rem2 = remain % 90, remain % 180
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


def update_role_info(user_id):
    flag, xqtd_uid = get_uid(user_id, 'xqtd_uid')
    if not flag:
        return False, r'请先绑定uid'
    req = requests.get(f'https://sr.ikechan8370.com/v1/info/{xqtd_uid}?lang=cn')
    if req.status_code != 200:
        return False, r'无法获取角色信息'
    try:
        data = req.json()['playerDetailInfo']
        role_list = data['displayAvatars']
        role_list.append(data['assistAvatar'])
        res = [role['name'] for role in role_list if insert_role_info(xqtd_uid, role)]
        return res != [], '无可更新角色' if res == [] else f'更新 {res} 成功. 使用"/xrole 角色名查看"'
    except Exception as e:
        logger.exception(f'{user_id}: {xqtd_uid} {req.text} {e}')
        return False, f'解析数据错误'


def get_role_info(user_id, role_name):
    flag, xqtd_uid = get_uid(user_id, 'xqtd_uid')
    if not flag:
        return False, r'请先绑定uid'

    role_id = name_to_id(role_name)
    if not role_id:
        return False, '检查角色名是否正确'

    res = select_role_info(xqtd_uid, role_id)
    if not res:
        return False, '未查询到角色信息, 使用 "/xupdate" 更新展柜角色信息'

    return True, gen_role_info(eval(res[0]['info']))


def gen_role_info(data: dict):
    role_name = data['name']
    role_rank = '' if data['rank'] == 0 else f"{data['rank']} 命"
    role_level = data['level']
    role_score = int(data['relic_score'])
    equip_name = data['equipment']['name']
    equip_level = data['equipment']['level']
    equip_rank = data['equipment']['rank']

    attr_info = gen_attr_info(data['properties'])

    skills = [f"[{skill['type']}]{skill['name']}: Lv{skill['level']}"
              for skill in data['behaviorList'] if 'type' in skill]
    skills = '\t'.join(skills[:3]) + '\n' + '\t'.join(skills[3:])

    # for relic in data['relics']:
    #     logger.debug(f"{'sub_affix_id' in relic} {relic}")
    relics = '\n'.join([f"{relic['name']}[+{relic['level']}]  "
                        f"{relic['main_affix_name']}: "
                        f"{parse_affix_value(relic['main_affix_value'])}"
                        f"  评分: {int(relic['score'])}\n"
                        f"{gen_sub_affix(relic['sub_affix_id'])}" for relic in data['relics']])

    return f'\n{role_name}: Lv{role_level} {role_rank}命\n' \
           f'{skills}\n{attr_info}\n' \
           f'\n{equip_name}: Lv{equip_level} 叠影{equip_rank}阶 遗器总评分: {role_score}\n{relics}'


def gen_attr_info(attr):
    base_atk = parse_affix_value(attr['attackBase'])
    delta_atk = parse_affix_value(attr['attackDelta'])
    total_atk = parse_affix_value(attr['attackBase'] + attr['attackDelta'])

    base_def = parse_affix_value(attr['defenseBase'])
    delta_def = parse_affix_value(attr['defenseDelta'])
    total_def = parse_affix_value(attr['defenseBase'] + attr['defenseDelta'])

    base_hp = parse_affix_value(attr['hpBase'])
    delta_hp = parse_affix_value(attr['hpDelta'])
    total_hp = parse_affix_value(attr['hpBase'] + attr['hpDelta'])

    base_speed = parse_affix_value(attr['speedBase'])
    add_speed = parse_affix_value(attr['speedAdd'])
    total_speed = parse_affix_value(attr['speedBase'] + attr['speedAdd'])

    critical_chance = parse_affix_value(attr['criticalChance'])
    critical_damage = parse_affix_value(attr['criticalDamage'])
    status_resistance = parse_affix_value(attr['statusResistance'])
    status_probability = parse_affix_value(attr['statusProbability'])
    break_damage_add = parse_affix_value(attr['breakDamageAdded'])
    heal_ratio = parse_affix_value(attr['healRatio'])
    sp_ratio = f"{int((attr['spRatio'] + 1) * 100)}%"
    damage_add = parse_affix_value(
        attr['physicalAdded'] + attr['fireAdded'] + attr['iceAdded'] +
        attr['thunderAdded'] + attr['windAdded'] + attr['quantumAdded'] + attr['imaginaryAdded'])

    return f'攻击力: {total_atk}({base_atk}+{delta_atk})\n' \
           f'防御力: {total_def}({base_def}+{delta_def})\n' \
           f'生命值: {total_hp}({base_hp}+{delta_hp})\n' \
           f'速度: {total_speed}({base_speed}+{add_speed})\t' \
           f'效果抵抗: {status_resistance}\t\t效果命中: {status_probability}\n' \
           f'暴击率: {critical_chance}\t\t暴击伤害: {critical_damage}\t\t击破特攻: {break_damage_add}\n' \
           f'治疗加成: {heal_ratio}\t\t能量回复: {sp_ratio}\t\t属性加成: {damage_add}'


def gen_sub_affix(affix_list):
    res = []
    for affix in affix_list:
        cnt = '' if affix['cnt'] == 1 else f"[{affix['cnt'] - 1}]"
        res.append(format_str(f"{cnt}{affix['name']}: {parse_affix_value(affix['value'])}"))
    return f"{res[0]}{res[1]}\n{res[2]}{res[3]}\n"


def parse_affix_value(value):
    if value > 2:
        return int(value)
    return f'{round(value * 100, 1)}%'


if __name__ == '__main__':
    pass
