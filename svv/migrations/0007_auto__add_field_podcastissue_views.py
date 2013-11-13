# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PodcastIssue.views'
        db.add_column('svv_podcastissue', 'views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PodcastIssue.views'
        db.delete_column('svv_podcastissue', 'views')


    models = {
        'svv.podcastissue': {
            'Meta': {'object_name': 'PodcastIssue', 'ordering': "('-pub_date', '-title')"},
            'celery_task': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '40'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_audio': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'length_video': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '1000'}),
            'skip_feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '1000'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['svv']