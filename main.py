import botpy

from bot import *
from utils import *


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

    async def on_message_create(self, message: Message):
        logger.info(f'guild: {message.guild_id} '
                    f'channel: {message.channel_id} '
                    f'author: {message.author} '
                    f'mentions: {message.mentions} '
                    f'content: {message.content}')

        if not check_cd(message.author.id):
            message.reply(content='cd...')

        handles = handle_list \
            if message.channel_id not in bot_list \
            else bot_list[message.channel_id].get_handles()
        for handle in handles:
            if await handle(api=self.api, message=message):
                return

    async def on_direct_message_create(self, message: DirectMessage):
        logger.info(f'author: {message.author} '
                    f'direct_message: {message.direct_message} '
                    f'content: {message.content}')

        if not check_cd(message.author.id):
            message.reply(content='cd...')

        for handle in direct_bot.get_handle():
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
