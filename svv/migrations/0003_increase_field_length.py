# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('svv', '0002_podcastissue_last_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcastissue',
            name='short_description',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='podcastissue',
            name='title',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
