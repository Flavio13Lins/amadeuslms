# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-21 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0008_remove_link_description_brief'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='link_url',
            field=models.CharField(max_length=250, verbose_name='Link_URL'),
        ),
    ]