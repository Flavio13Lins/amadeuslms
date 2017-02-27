# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-24 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pendencies', '0005_auto_20170201_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendencies',
            name='action',
            field=models.CharField(blank=True, choices=[('view', 'Visualize'), ('create', 'Create'), ('answer', 'Answer'), ('access', 'Access'), ('finish', 'Finish'), ('submit', 'Submit')], max_length=100, verbose_name='Action'),
        ),
    ]