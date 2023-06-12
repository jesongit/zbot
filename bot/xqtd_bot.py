from botpy import BotAPI
from botpy.message import Message
from botpy.ext.command_util import Commands

from api import *


@Commands("help")
async def get_gacha_help(api: BotAPI, message: Message, params=None):
    await message.reply(file_image='res/img/xqtd_help_url.png',
                        content=f'<@{message.author.id}>私聊机器人"/xurl url"获取抽卡记录，抽卡记录链接教程：')
    return True


@Commands("bind")
async def bind_user(api: BotAPI, message: Message, params: str = None):
    if not params.isdecimal() or len(params) != 9:
        info = 'uid格式错误'
    else:
        _, info = user.update(message.author.id, 'xqtd_uid', int(params))
    await message.reply(content=f'<@{message.author.id}>bind: {params}, {info}')
    return True


@Commands("gc")
async def gacha_record(api: BotAPI, message: Message, params: str = None):
    flag, info = xqtd_gacha_info(message)
    info = '请先使用"/bind uid"绑定uid' if not flag else info
    await message.reply(content=f'<@{message.author.id}>{info}')
    return True


def xqtd_gacha_info(message):
    flag, xqtd_uid = user.get_uid(message.author.id, 'xqtd_uid')
    return flag, '' if not flag else gen_gacha_info(xqtd_uid)


def get_handles():
    return [get_gacha_help, bind_user, gacha_record]


if __name__ == '__main__':
    pass
