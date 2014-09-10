# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PodcastIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('short_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('file', models.FileField(upload_to='mp3', blank=True, null=True)),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('youtube_url', models.URLField()),
                ('skip_feed', models.BooleanField(default=False)),
                ('celery_task', models.CharField(blank=True, max_length=40, null=True)),
                ('length_video', models.IntegerField(default=0)),
                ('length_audio', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-pub_date', '-title'),
            },
            bases=(models.Model,),
        ),
    ]
