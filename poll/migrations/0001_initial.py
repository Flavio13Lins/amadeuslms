# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-16 20:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200, verbose_name='Answer')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
            ],
            options={
                'verbose_name_plural': 'Answers',
                'ordering': ('order',),
                'verbose_name': 'Answer',
            },
        ),
        migrations.CreateModel(
            name='AnswersStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Answered')),
                ('answered_in', models.DateTimeField(auto_now=True, verbose_name='Answered Date')),
                ('answer', models.ManyToManyField(related_name='answers_stundet', to='poll.Answer', verbose_name='Answers Students')),
            ],
            options={
                'verbose_name_plural': 'Answers Student',
                'verbose_name': 'Answer Stundent',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.Activity')),
            ],
            options={
                'verbose_name_plural': 'Polls',
                'verbose_name': 'Poll',
            },
            bases=('courses.activity',),
        ),
        migrations.AddField(
            model_name='answersstudent',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_stundet', to='poll.Poll', verbose_name='Poll'),
        ),
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
