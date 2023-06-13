from api import *
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message, DirectMessage

TEXT_HELP = '请先导入抽卡记录\n1. 图片连接查看获取抽卡链接教程.\n2. 私聊"/xurl 抽卡链接" 导入抽卡记录'
TEXT_BIND = '未绑定uid, 请使用"/bind uid" 进行绑定'

IMG_URL_HELP = 'res/img/xqtd_help_url.png'


@Commands("bind")
async def bind_user(api: BotAPI, message: Message, params: str = None):
    if not params.isdecimal() or len(params) != 9:
        info = 'uid格式错误'
    else:
        _, info = user.update_key_val(message.author.id, 'xqtd_uid', int(params))
    await message.reply(content=f'<@{message.author.id}>bind: {params}, {info}')
    return True


@Commands("gc")
async def gacha_record(api: BotAPI, message: Message, params: str = None):
    img, info = xqtd_gacha_info(message.author.id)
    await message.reply(content=f'<@{message.author.id}>{info}', file_image=img)
    return True


@Commands("/xurl")
async def load_xqtd_url(api: BotAPI, message: DirectMessage, params: str = None):
    flag, authkey, game_biz = parse_web_url(params)
    if flag:
        load_all_gache_record(authkey, game_biz)
        img, info = xqtd_gacha_info(message.author.id)
        await message.reply(content=f'<@{message.author.id}>{info}', file_image=img)
    else:
        await message.reply(content=f'<@{message.author.id}>url格式错误.')
    return True


def xqtd_gacha_info(user_id: str):
    flag, xqtd_uid = user.get_uid(user_id, 'xqtd_uid')
    if not flag:
        return None, TEXT_BIND
    flag, info = gen_gacha_info(xqtd_uid)
    if not flag:
        return IMG_URL_HELP, TEXT_HELP
    return None, info


def get_handles():
    return [bind_user, gacha_record, load_xqtd_url]


if __name__ == '__main__':
    pass
