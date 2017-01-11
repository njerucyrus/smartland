# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0010_landpurchases_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='land',
            options={'verbose_name_plural': 'Lands'},
        ),
        migrations.AlterModelOptions(
            name='landtransfers',
            options={'verbose_name_plural': 'LandTransfers'},
        ),
        migrations.AlterModelOptions(
            name='landuserprofile',
            options={'verbose_name_plural': 'LandUserProfiles'},
        ),
    ]
