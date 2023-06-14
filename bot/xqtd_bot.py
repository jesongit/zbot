#!/usr/bin/python
# -*- coding: UTF-8 -*-
from api import *
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message, DirectMessage

TEXT_URL_HELP = '请先导入抽卡记录\n1. 图片连接查看获取抽卡链接教程.\n2. 私聊"/xurl 抽卡链接" 导入抽卡记录'
TEXT_BIND = '未绑定uid, 请使用"/bind uid" 进行绑定'
TEXT_HELP = f'''
星穹铁道相关指令：
/xhelp: 查看所有指令
/xurl: 使用抽卡链接导入抽卡记录 导入后自动绑定uid
/xgacha: 查看抽卡记录
'''

IMG_URL_HELP = 'res/img/xqtd_help_url.png'


@Commands("xbind")
async def bind_user(api: BotAPI, message: Message, params: str = None):
    if not params.isdecimal() or len(params) != 9:
        info = 'uid格式错误'
    else:
        _, info = user.update_key_val(message.author.id, 'xqtd_uid', int(params))
    await message.reply(content=f'<@{message.author.id}>bind: {params}, {info}')
    return True


@Commands("xgacha")
async def gacha_record(api: BotAPI, message: Message, params: str = None):
    img, info = xqtd_gacha_info(message.author.id)
    await message.reply(content=f'<@{message.author.id}>{info}', file_image=img)
    return True


@Commands("xurl")
async def load_xqtd_url(api: BotAPI, message: DirectMessage, params: str = None):
    flag, authkey, game_biz = parse_web_url(params)
    if flag:
        xqtd_uid = load_all_gache_record(authkey, game_biz)
        update_key_val(message.author.id, 'xqtd_uid', xqtd_uid)
        img, info = xqtd_gacha_info(message.author.id)
        await message.reply(content=f'<@{message.author.id}>绑定uid: {xqtd_uid}\n{info}', file_image=img)
    else:
        await message.reply(content=f'<@{message.author.id}>url格式错误.')
    return True


@Commands("xhelp")
async def load_xqtd_url(api: BotAPI, message: DirectMessage, params: str = None):
    await message.reply(content=f'<@{message.author.id}>{TEXT_HELP}')
    return True


def xqtd_gacha_info(user_id: str):
    flag, xqtd_uid = user.get_uid(user_id, 'xqtd_uid')
    if not flag:
        return None, TEXT_BIND
    flag, info = gen_gacha_info(xqtd_uid)
    if not flag:
        return IMG_URL_HELP, TEXT_URL_HELP
    return None, info


def get_handles():
    return [bind_user, gacha_record, load_xqtd_url]


if __name__ == '__main__':
    pass
