from django.contrib.auth.models import User
from django.db import models
# from django.db.models import signals
# from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_TYPES = (
        ('man', '男性'),
        ('woman', '女性'),
        ('other', '其他'),
        ('privacy', '隐私'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nikename = models.CharField(max_length=255, default='', blank=True, null=True, help_text='别名')
    mobile_no = models.CharField(max_length=255, unique=True, help_text='手机号')
    gender = models.CharField(max_length=255, choices=GENDER_TYPES, default='privacy', help_text='性别')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{user} {nikename} {mobile_no}'.format(user=self.user.username,
                                                      nikename=self.nikename,
                                                      mobile_no=self.mobile_no)


class CheckImage(models.Model):
    image_id = models.CharField(max_length=255, primary_key=True, help_text='图片Id')
    image_value = models.CharField(max_length=255, help_text='图片值')
    is_valid = models.BooleanField(default=True, help_text='验证码是否有效')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{image_id} {image_value}'.format(image_id=self.image_id, image_value=self.image_value)


# @receiver(signals.post_save, sender=UserProfile)
# def post_save_userprofile(sender, instance, created, **kwargs):
#     pass
