# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('land', '0009_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpurchases',
            name='owner',
            field=models.ForeignKey(default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
