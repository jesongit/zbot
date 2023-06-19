#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from PIL import Image
from botpy import logger

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


def fill_tab(s: str):
    logger.debug(f"len: {len(s)} {len(s.encode('gbk'))}{s}")
    s = s.encode('gbk')
    if len(s) < 8:
        return '\t'
    if len(s) < 16:
        return ''
    return ''


def format_str(s: str):
    logger.debug(f'len: {len(s)} {len(s.encode("utf8"))} {s}')
    length = len(s.encode('gbk'))
    tab_cnt = int((32 - length) // 4 + 0.5)
    # if length % 4 == 0:
    #     tab_cnt -= 1
    return s + '\t' * tab_cnt
    # if len(l) <= 4:
    #     return f'{s}\t\t\t\t\t'
    # if len(l) <= 8:
    #     return f'{s}\t\t\t\t'
    # if len(l) <= 12:
    #     return f'{s}\t\t\t'
    # if len(l) <= 16:
    #     return f'{s}\t\t'
    # if len(l) <= 20:
    #     return f"{s}\t"
    # return s
