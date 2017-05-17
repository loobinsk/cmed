# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Settings.spam_report_email'
        db.add_column(u'Settings', 'spam_report_email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Settings.spam_report_period'
        db.add_column(u'Settings', 'spam_report_period',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Settings.spam_report_email'
        db.delete_column(u'Settings', 'spam_report_email')

        # Deleting field 'Settings.spam_report_period'
        db.delete_column(u'Settings', 'spam_report_period')


    models = {
        u'medtus.translation': {
            'Meta': {'object_name': 'Translation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data': ('tinymce.models.HTMLField', [], {'default': 'None', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u0422\\u0440\\u0430\\u043d\\u0441\\u043b\\u044f\\u0446\\u0438\\u044f'", 'max_length': '255'})
        },
        u'settings.settings': {
            'Meta': {'object_name': 'Settings', 'db_table': "u'Settings'"},
            'agreement': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spam_report_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'spam_report_period': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['medtus.Translation']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'})
        },
        u'settings.socialicons': {
            'Meta': {'object_name': 'SocialIcons'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['settings']