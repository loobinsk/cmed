# -*- coding: utf-8 -*-

from PIL import Image
from wand.image import Image as WandImage
from django.conf import settings

size = settings.AVATAR_SIZE

def is_image_animated(img):
    try:
        img.seek(1)
    except EOFError:
        isanimated = False
    else:
        isanimated = True
    return isanimated

def resize_and_crop(img_path, modified_path, size, crop_type='top'):
    """
    Resize and crop an image to fit the specified size.

    args:
        img_path: path for the image to resize.
        modified_path: path to store the modified image.
        size: `(width, height)` tuple.
        crop_type: can be 'top', 'middle' or 'bottom', depending on this
            value, the image will cropped getting the 'top/left', 'midle' or
            'bottom/rigth' of the image to fit the size.
    raises:
        Exception: if can not open the file in img_path of there is problems
            to save the image.
        ValueError: if an invalid `crop_type` is provided.
    """
    # If height is higher we resize vertically, if not we resize horizontally
    img = Image.open(img_path)
    isanimated = is_image_animated(img)
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    box = None
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        new_x_size = size[0]
        new_y_size = size[0] * img.size[1] / img.size[0]
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, new_x_size, size[1])
        elif crop_type == 'middle':
            box = (0, (new_y_size - size[1]) / 2, new_x_size, (new_y_size + size[1]) / 2)
        elif crop_type == 'bottom':
            box = (0, new_y_size - size[1], new_x_size, new_y_size)
        else :
            raise ValueError('ERROR: invalid value for crop_type')
    elif ratio < img_ratio:
        new_x_size = size[1] * img.size[0] / img.size[1]
        new_y_size = size[1]
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], new_y_size)
        elif crop_type == 'middle':
            box = ((new_x_size - size[0]) / 2, 0, (new_x_size + size[0]) / 2, new_y_size)
        elif crop_type == 'bottom':
            box = (new_x_size - size[0], 0, new_x_size, new_y_size)
        else:
            raise ValueError('ERROR: invalid value for crop_type')
    else:
        new_x_size = size[0]
        new_y_size = size[1]
        # If the scale is the same, we do not need to crop

    if isanimated:
        with WandImage(filename=img_path) as img:
            img.resize(new_x_size, new_y_size)
            if box:
                img = img.crop(box)
            f = open(modified_path, 'w')
            img.save(file=f)
    else:
        img = img.resize((new_x_size, new_y_size), Image.ANTIALIAS)
        if box:
            img = img.crop(box)
        img.save(modified_path)
