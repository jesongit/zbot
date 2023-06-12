from bot import *
from botpy.message import DirectMessage


@Commands("test")
async def test(api: BotAPI, message: DirectMessage, params: str = None):
    await message.reply(content=f'params: {params}')
    return True


@Commands("/xurl")
async def load_xqtd_url(api: BotAPI, message: DirectMessage, params: str = None):
    flag, authkey, game_biz = parse_web_url(params)
    if flag:
        await message.reply(content=f'开始获取抽卡记录.')
        load_all_gache_record(authkey, game_biz)
        flag, info = xqtd_gacha_info(message)
        await message.reply(content=f'获取完成.{info}')
    else:
        await message.reply(content=f'url格式错误.')
    return True


def get_handle():
    return [test, load_xqtd_url]
