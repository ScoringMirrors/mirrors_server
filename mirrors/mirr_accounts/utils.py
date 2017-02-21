import os
from django.utils import timezone

from base64 import b64encode
from hashlib import md5, sha1, sha256
from django.conf import settings
from random import sample
from wheezy.captcha.image import (captcha, background, curve, noise, smooth,
                                  text, offset, rotate, warp)

from .models import CheckImage


def create_check_image(timestamp):
    image_drawings = [
        background(),
        text(fonts=[os.path.join(settings.CHECK_IMAGE_FONTS_PATH, font_path)
                    for font_path in os.listdir(settings.CHECK_IMAGE_FONTS_PATH)],
             drawings=[warp(), rotate(), offset()]),
        curve(number=4),
        noise(),
        smooth(), ]
    image_layout = captcha(drawings=image_drawings)

    value = sample(settings.CHECK_STR, 4)
    image_file = 'tmp_check_{}.JPEG'.format(timestamp)
    image_layout(value).save(image_file)
    with open(image_file, 'rb') as f:
        image_base64 = b64encode(f.read())
        os.remove(image_file)
    image_id = '{}{}'.format(md5(sha1(image_base64).hexdigest().encode('utf-8')).hexdigest(), timestamp)
    image, is_image = CheckImage.objects.get_or_create(image_id=image_id, image_value=''.join(value))
    if is_image is False:
        return create_check_image(timestamp)
    return (image.image_id, image_base64.decode('utf-8'))


def validity_check_image(image_id, image_value):
    try:
        image = CheckImage.objects.filter(image_id=image_id)
    except Exception:
        return (CheckImage.objects.none(), False)

    if image.exists() is False:
        return (image, False)

    image = image.last()
    if image.is_valid is False:
        return (image, False)
    is_valid_time = (timezone.now() - image.created_at).total_seconds()
    if is_valid_time < 0 or is_valid_time > 600 or image.image_value != image_value:
        image.delete()
        return (image, False)

    image.is_valid = False
    image.save()
    return (image, True)


def create_register_token(ip, image_id):
    image = CheckImage.objects.filter(image_id=image_id)
    if image.exists() is False:
        return ''
    image = image.last()
    if image.is_valid:
        return ''
    image.image_value = sha256(bytes('{}{}{}'.format(ip, settings.SECRET_KEY, image_id), 'utf-8')).hexdigest()
    image.save()
    return image.image_value


def validity_register_token(ip, image_id, register_token):
    image = CheckImage.objects.filter(image_id=image_id)
    if image.exists() is False:
        return False
    image = image.last()
    if image.is_valid:
        return False
    if image.image_value == register_token:
        image.delete()
        return True
    return False


def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        return ip
    return request.META.get('REMOTE_ADDR')
