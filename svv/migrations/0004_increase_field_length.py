# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svv', '0003_increase_field_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcastissue',
            name='short_description',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='podcastissue',
            name='title',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
