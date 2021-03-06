# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-10 05:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('audio_track_type', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'app_audio_track',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('lesson_num', models.CharField(max_length=10)),
                ('lesson_title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('level', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_version', models.CharField(max_length=64)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sentences', to='app.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='SentenceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('text', models.TextField()),
                ('audio_url', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('sentence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sentence_lines', to='app.Sentence')),
            ],
            options={
                'db_table': 'app_sentence_line',
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='app.Season'),
        ),
        migrations.AddField(
            model_name='audiotrack',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audio_tracks', to='app.Lesson'),
        ),
    ]
