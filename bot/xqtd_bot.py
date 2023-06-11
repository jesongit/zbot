from botpy import BotAPI
from botpy.message import Message
from botpy.ext.command_util import Commands

import db.user
from api.xqtd_api import load_all_gache_record, parse_web_url, gen_gacha_info


@Commands("help")
async def get_gacha_help(api: BotAPI, message: Message, params=None):
    await message.reply(content=f'<@{message.author.id}>获取抽卡记录链接教程：', file_image='res/xqtd_help_url.png')
    return True


@Commands("bind")
async def bind_user(api: BotAPI, message: Message, params: str = None):
    if not params.isdecimal() or len(params) != 9:
        info = 'uid格式错误'
    else:
        _, info = db.user.update(message.author.id, 'xqtd_uid', int(params))
    await message.reply(content=f'<@{message.author.id}>bind: {params}, {info}')
    return True


@Commands("gc")
async def gacha_record(api: BotAPI, message: Message, params: str = None):
    flag, info = gacha_info(message)
    info = '请先使用"/bind uid"绑定uid' if not flag else info
    await message.reply(content=f'<@{message.author.id}>{info}')
    return True


@Commands("url")
async def load_url(api: BotAPI, message: Message, params: str = None):
    flag, authkey, game_biz = parse_web_url(params)
    if flag:
        await message.reply(content=f'<@{message.author.id}>开始获取抽卡记录.')
        load_all_gache_record(authkey, game_biz)
        flag, info = gacha_info(message)
        await message.reply(content=f'<@{message.author.id}>获取完成.{info}')
    else:
        await message.reply(content=f'<@{message.author.id}>url格式错误.')
    return True


def gacha_info(message: Message):
    flag, xqtd_uid = db.user.get_uid(message.author.id, 'xqtd_uid')
    return flag, '' if not flag else gen_gacha_info(xqtd_uid)


def get_handles():
    return [get_gacha_help, bind_user, gacha_record, load_url]


if __name__ == '__main__':
    pass
