# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Settings.agreement'
        db.add_column(u'Settings', 'agreement',
                      self.gf('tinymce.models.HTMLField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Settings.agreement'
        db.delete_column(u'Settings', 'agreement')


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
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['medtus.Translation']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'})
        }
    }

    complete_apps = ['settings']