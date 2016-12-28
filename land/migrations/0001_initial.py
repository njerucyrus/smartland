# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_deed', models.CharField(max_length=32)),
                ('location', models.CharField(max_length=128)),
                ('size', models.FloatField()),
                ('photo', models.ImageField(upload_to=b'land/images/')),
                ('description', models.TextField(max_length=140)),
                ('on_sale', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LandTransfers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_title_deed', models.CharField(max_length=32)),
                ('size_transferred', models.FloatField()),
                ('relationship', models.CharField(max_length=64)),
                ('date_transferred', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LandUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_no', models.PositiveIntegerField(unique=True, db_index=True)),
                ('phone_number', models.CharField(unique=True, max_length=13)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='landtransfers',
            name='owner',
            field=models.ForeignKey(to='land.LandUserProfile'),
        ),
        migrations.AddField(
            model_name='landtransfers',
            name='title_deed',
            field=models.ForeignKey(related_name='LandTransfers', to='land.Land'),
        ),
        migrations.AddField(
            model_name='landtransfers',
            name='transferred_to',
            field=models.ForeignKey(related_name='TransferredTo', to='land.LandUserProfile'),
        ),
        migrations.AddField(
            model_name='land',
            name='user',
            field=models.ForeignKey(to='land.LandUserProfile'),
        ),
    ]
