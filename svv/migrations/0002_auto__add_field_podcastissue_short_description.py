# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PodcastIssue.short_description'
        db.add_column('svv_podcastissue', 'short_description',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=1000, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PodcastIssue.short_description'
        db.delete_column('svv_podcastissue', 'short_description')


    models = {
        'svv.podcastissue': {
            'Meta': {'object_name': 'PodcastIssue'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '1000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '1000', 'blank': 'True'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['svv']