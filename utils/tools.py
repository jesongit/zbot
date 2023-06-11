import logging

import yaml
from pathlib import Path

from PIL import Image

config = yaml.safe_load(Path('config.yaml').open(encoding='utf8'))


def appid():
    return config['appid']


def token():
    return config['token']


def log_level():
    return config['log_level']


def join_img(img_list):
    pre_width, height, width = 0, max([im.size[1] for im in img_list]), sum([im.size[0] for im in img_list])
    logging.info(f'{pre_width}, {height}, {width}')
    bg = Image.new("RGB", (width, height))
    for im in img_list:
        bg.paste(im, (pre_width, 0))
        pre_width += im.size[0]
    return bg
