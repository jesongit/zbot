#!/usr/bin/python
# -*- coding: UTF-8 -*-
from api import *

import botpy
from botpy import logger
from botpy.message import Message, DirectMessage


class ZBot(botpy.Client):

    def __init__(self, check_message, handle_list, **kwargs):
        super().__init__(**kwargs)
        self.handle_list = handle_list
        self.check_message = check_message

    async def on_message_create(self, message: Message):
        logger.info(f'guild: {message.guild_id} '
                    f'channel: {message.channel_id} '
                    f'author: {message.author} '
                    f'mentions: {message.mentions} '
                    f'content: {message.content}')

        if not self.check_message(message):
            return
        for handle in self.handle_list['on_message_create']:
            if await handle(api=self.api, message=message):
                return

    async def on_direct_message_create(self, message: DirectMessage):
        logger.info(f'author: {message.author} '
                    f'direct_message: {message.direct_message} '
                    f'content: {message.content}')

        if not self.check_message(message):
            return
        for handle in self.handle_list['on_direct_message_create']:
            if await handle(api=self.api, message=message):
                return
