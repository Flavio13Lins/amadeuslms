# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-13 05:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answersstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_stundent', to=settings.AUTH_USER_MODEL, verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='poll.Poll', verbose_name='Answers'),
        ),
    ]
