# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PodcastIssue.length_video'
        db.add_column('svv_podcastissue', 'length_video',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PodcastIssue.length_audio'
        db.add_column('svv_podcastissue', 'length_audio',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PodcastIssue.length_video'
        db.delete_column('svv_podcastissue', 'length_video')

        # Deleting field 'PodcastIssue.length_audio'
        db.delete_column('svv_podcastissue', 'length_audio')


    models = {
        'svv.podcastissue': {
            'Meta': {'object_name': 'PodcastIssue', 'ordering': "('-pub_date', '-title')"},
            'celery_task': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '40'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_audio': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'length_video': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1000'}),
            'skip_feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1000'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['svv']