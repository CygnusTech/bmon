# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-06 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmsapp', '0019_auto_20170329_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodicscript',
            name='period',
            field=models.IntegerField(choices=[(0, b'Disabled'), (300, b'5 min'), (600, b'10 min'), (900, b'15 min'), (1800, b'30 min'), (3600, b'1 hr'), (7200, b'2 hr'), (14400, b'4 hr'), (21600, b'6 hr'), (43200, b'12 hr'), (86400, b'24 hr')], default=3600, verbose_name=b'How often should script run'),
        ),
    ]
