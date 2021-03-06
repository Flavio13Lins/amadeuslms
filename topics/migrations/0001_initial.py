# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-16 18:59
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subjects', '0012_auto_20170112_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('repository', models.BooleanField(default=False, verbose_name='Repository')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Last Update')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_subject', to='subjects.Subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
    ]
