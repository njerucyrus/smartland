# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0025_landuserprofile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='title_deed_scan',
            field=models.FileField(default='', upload_to=b'land/files/'),
            preserve_default=False,
        ),
    ]
