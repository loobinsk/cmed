# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lecturer'
        db.create_table(u'lecturers_lecturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('secondname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('tinymce.models.HTMLField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'lecturers', ['Lecturer'])

        # Adding model 'LecturerLink'
        db.create_table(u'lecturers_lecturerlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lecturer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['lecturers.Lecturer'])),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'lecturers', ['LecturerLink'])


    def backwards(self, orm):
        # Deleting model 'Lecturer'
        db.delete_table(u'lecturers_lecturer')

        # Deleting model 'LecturerLink'
        db.delete_table(u'lecturers_lecturerlink')


    models = {
        u'lecturers.lecturer': {
            'Meta': {'object_name': 'Lecturer'},
            'content': ('tinymce.models.HTMLField', [], {}),
            'createdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'secondname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'lecturers.lecturerlink': {
            'Meta': {'object_name': 'LecturerLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecturer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': u"orm['lecturers.Lecturer']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['lecturers']