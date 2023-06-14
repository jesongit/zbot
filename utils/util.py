#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

from PIL import Image


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
