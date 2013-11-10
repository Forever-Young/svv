# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PodcastIssue.skip_feed'
        db.add_column('svv_podcastissue', 'skip_feed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PodcastIssue.skip_feed'
        db.delete_column('svv_podcastissue', 'skip_feed')


    models = {
        'svv.podcastissue': {
            'Meta': {'object_name': 'PodcastIssue', 'ordering': "('-pub_date', '-title')"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1000', 'null': 'True'}),
            'skip_feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1000', 'null': 'True'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['svv']