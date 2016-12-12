# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-24 15:17
from __future__ import unicode_literals

import autoslug.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name': 'Action',
                'verbose_name_plural': 'Actions',
            },
        ),
        migrations.CreateModel(
            name='Action_Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Action_Resource',
                'verbose_name_plural': 'Action_Resources',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.TextField(verbose_name='Component (Module / App)')),
                ('context', django.contrib.postgres.fields.jsonb.JSONField(blank=True, verbose_name='Context')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time of action')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='MimeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=100, unique=True, verbose_name='Type')),
                ('icon', models.CharField(max_length=50, unique=True, verbose_name='Icon')),
            ],
            options={
                'verbose_name': 'Amadeus Mime Type',
                'verbose_name_plural': 'Amadeus Mime Types',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time of action')),
                ('action_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Action_Resource', verbose_name='Action_Resource')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('url', models.CharField(default='', max_length=100, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
        ),
    ]
