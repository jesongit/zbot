#!/usr/bin/python
# -*- coding: UTF-8 -*-
from botpy import BotAPI
from botpy.message import DirectMessage
from botpy.ext.command_util import Commands


@Commands("/echo")
async def echo(api: BotAPI, message: DirectMessage, params: str = None):
    await message.reply(content=params)
    return True


def get_handles():
    return [echo]
