# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-02 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmsapp', '0020_auto_20170406_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='other_properties',
            field=models.TextField(blank=True, help_text=b'One property per line.  Name of Property, a colon, a space, and then the property value.', verbose_name=b'Additional Properties to include when exporting data. YAML form, e.g. age: 23'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='other_properties',
            field=models.TextField(blank=True, help_text=b'One property per line.  Name of Property, a colon, a space, and then the property value.', verbose_name=b'Additional Properties to include when exporting data. YAML form, e.g. room: telecom closet'),
        ),
    ]
