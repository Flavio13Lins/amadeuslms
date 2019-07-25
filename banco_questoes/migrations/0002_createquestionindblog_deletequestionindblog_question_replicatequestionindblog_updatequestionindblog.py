# Generated by Django 2.2 on 2019-06-21 15:19

import banco_questoes.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('log', '0001_initial'),
        ('banco_questoes', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateQuestionInDBLog',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='log.Log')),
            ],
            bases=('log.log',),
        ),
        migrations.CreateModel(
            name='DeleteQuestionInDBLog',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='log.Log')),
            ],
            bases=('log.log',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField(blank=True, verbose_name='Statement')),
                ('question_img', models.ImageField(blank=True, null=True, upload_to='questions/', validators=[banco_questoes.models.validate_img_extension], verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='ReplicateQuestionInDBLog',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='log.Log')),
            ],
            bases=('log.log',),
        ),
        migrations.CreateModel(
            name='UpdateQuestionInDBLog',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='log.Log')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco_questoes.Question')),
            ],
            bases=('log.log',),
        ),
    ]