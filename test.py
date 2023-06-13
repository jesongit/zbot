from bot import *
from utils import *

handle_list = {
    'on_message_create': xqtd_bot.get_handles(),
    'on_direct_message_create': direct_bot.get_handles(),
}


def check_message(message):
    if isinstance(message, DirectMessage):
        return True
    return message.channel_id == test_channel()


def start_bot():
    intents = botpy.Intents(guild_messages=True, direct_message=True)
    client = ZBot(check_message, handle_list, intents=intents, log_level=10)
    client.run(appid=appid(), token=token())


if __name__ == '__main__':
    start_bot()
