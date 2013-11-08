# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PodcastIssue'
        db.create_table('svv_podcastissue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(null=True, max_length=1000, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(null=True, max_length=100, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('youtube_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('svv', ['PodcastIssue'])


    def backwards(self, orm):
        # Deleting model 'PodcastIssue'
        db.delete_table('svv_podcastissue')


    models = {
        'svv.podcastissue': {
            'Meta': {'object_name': 'PodcastIssue'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '1000', 'blank': 'True'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['svv']