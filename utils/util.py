from PIL import Image


def join_img(img_list):
    pre_width, height, width = 0, max([im.size[1] for im in img_list]), sum([im.size[0] for im in img_list])
    bg = Image.new("RGB", (width, height))
    for im in img_list:
        bg.paste(im, (pre_width, 0))
        pre_width += im.size[0]
    return bg
