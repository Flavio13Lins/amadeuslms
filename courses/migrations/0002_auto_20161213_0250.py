# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-13 05:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='professors',
            field=models.ManyToManyField(related_name='professors_subjects', to=settings.AUTH_USER_MODEL, verbose_name='Professors'),
        ),
        migrations.AddField(
            model_name='subject',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='subject_student', to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='material',
            name='students',
            field=models.ManyToManyField(related_name='materials', to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='material',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.Topic', verbose_name='Topic'),
        ),
        migrations.AddField(
            model_name='linkmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_link', to='courses.Material', verbose_name='Material'),
        ),
        migrations.AddField(
            model_name='filematerial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_file', to='courses.Material', verbose_name='Material'),
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_category', to='courses.CourseCategory', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='course',
            name='coordenator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_coordenator', to=settings.AUTH_USER_MODEL, verbose_name='Coordenator'),
        ),
        migrations.AddField(
            model_name='course',
            name='professors',
            field=models.ManyToManyField(related_name='courses_professors', to=settings.AUTH_USER_MODEL, verbose_name='Professors'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='courses_student', to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='activityfile',
            name='diet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='courses.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='students',
            field=models.ManyToManyField(related_name='activities', to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='activity',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='courses.Topic', verbose_name='Topic'),
        ),
    ]
