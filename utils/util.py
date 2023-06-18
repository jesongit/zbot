#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PIL import Image

LOG_MAX_BYTE = 10485760
LOG_FILE_CNT = 10


def join_img(img_list):
    pre_width, height, width = 0, max([im.size[1] for im in img_list]), sum([im.size[0] for im in img_list])
    bg = Image.new("RGB", (width, height))
    for im in img_list:
        bg.paste(im, (pre_width, 0))
        pre_width += im.size[0]
    return bg


def encode_powershell_str(s: str):
    s = s.encode('unicode_escape').decode()
    return ''.join([f'$([char]0x{c})' for c in s.split(r'\u') if c])


def decode_powershell_str(s: str):
    s = ''.join([f'\\u{c}' for c in re.findall(r'0x(.*?)\)', s)])
    return s.encode().decode('unicode_escape')


def logconfig(name: str = 'test'):
    Path('log').mkdir(parents=True, exist_ok=True)
    format = "%(asctime)-15s %(threadName)s[%(module)-6s:%(funcName)-10s %(lineno)-3d] %(levelname)s: %(message)s"

    info_handler = RotatingFileHandler(
        f'log/info_{name}.log', encoding='utf8', maxBytes=LOG_MAX_BYTE, backupCount=LOG_FILE_CNT)
    info_handler.setFormatter(logging.Formatter(format))
    info_handler.setLevel(logging.INFO)

    error_handler = RotatingFileHandler(
        f'log/error_{name}.log', encoding='utf8', maxBytes=LOG_MAX_BYTE, backupCount=LOG_FILE_CNT)
    error_handler.setFormatter(logging.Formatter(format))
    error_handler.setLevel(logging.ERROR)

    logging.basicConfig(level=logging.DEBUG, handlers=[info_handler, error_handler])
