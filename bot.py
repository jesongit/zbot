from bot import *
from utils import *

user_cd_dict = {}
handle_list = {
    'on_message_create': xqtd_bot.get_handles(),
    'on_direct_message_create': direct_bot.get_handles(),
}


def check_message(message):
    # 私聊通过
    if isinstance(message, DirectMessage):
        return True
    # 忽略测试频道消息
    if message.channel_id == test_channel():
        return False

    user_id = message.author.id
    now = time.time()
    if user_cd_dict.get(user_id) is None:
        return True
    user_cd_dict[user_id] = now + 3
    return user_cd_dict[user_id] < now


if __name__ == '__main__':
    intents = botpy.Intents(guild_messages=True, direct_message=True)
    client = ZBot(check_message, handle_list, intents=intents, log_level=log_level())
    client.run(appid=appid(), token=token())
