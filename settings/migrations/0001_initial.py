# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Settings'
        db.create_table(u'Settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('online', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'settings', ['Settings'])


    def backwards(self, orm):
        # Deleting model 'Settings'
        db.delete_table(u'Settings')


    models = {
        u'settings.settings': {
            'Meta': {'object_name': 'Settings', 'db_table': "u'Settings'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['settings']