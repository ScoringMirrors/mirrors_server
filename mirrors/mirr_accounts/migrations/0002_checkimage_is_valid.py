# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mirr_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkimage',
            name='is_valid',
            field=models.BooleanField(default=True, help_text='验证码是否有效'),
        ),
    ]
