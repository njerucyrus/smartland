# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0015_notification_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
