# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-25 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20161124_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='begin_exam',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Begin of Exam'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='end_exam',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='End of Exam'),
            preserve_default=False,
        ),
    ]
