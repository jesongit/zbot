import time
import botpy

from bot import xqtd_bot
from botpy import logger, BotAPI
from botpy.message import Message
from botpy.ext.command_util import Commands
from utils.tools import token, appid, log_level


@Commands("test")
async def test(api: BotAPI, message: Message, params: str = None):
    await message.reply(content=f'<@{message.author.id}>params: {params}')
    return True

bot_list = {
    '537729935': xqtd_bot,
}
handle_list = [test]

user_cd_dict = {}


class ZBot(botpy.Client):
    async def on_at_message_create(self, message: Message):
        logger.info(f'guild: {message.guild_id} channel: {message.channel_id} author: {message.author} mentions: {message.mentions} content: {message.content}')

        if not check_cd(message.author.id):
            logger.debug(f'in cd.')
            return

        handles = handle_list \
            if message.channel_id not in bot_list \
            else bot_list[message.channel_id].get_handles()
        for handle in handles:
            if await handle(api=self.api, message=message):
                return


def check_cd(user_id):
    now = time.time()
    if user_cd_dict.get(user_id) is None:
        return True
    user_cd_dict[user_id] = now + 3
    return user_cd_dict[user_id] < now


if __name__ == '__main__':
    intents = botpy.Intents.all()
    client = ZBot(intents=intents, log_level=log_level())
    client.run(appid=appid(), token=token())
