# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Categorys'
        db.delete_table(u'rss_categorys')


    def backwards(self, orm):
        # Adding model 'Categorys'
        db.create_table(u'rss_categorys', (
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('words', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('passval', self.gf('django.db.models.fields.IntegerField')(default=30)),
        ))
        db.send_create_signal(u'rss', ['Categorys'])


    models = {
        u'medtus.specialities': {
            'Meta': {'object_name': 'Specialities', 'db_table': "u'Specialities'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'passval': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'words': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'rss.feeds': {
            'Meta': {'object_name': 'Feeds'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rss.Filters']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'rss.filters': {
            'Meta': {'object_name': 'Filters'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'passval': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'words': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'rss.posts': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Posts'},
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment_cnt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment_show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'createdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rss.Feeds']"}),
            'format': ('django.db.models.fields.IntegerField', [], {}),
            'href': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'popular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_cmedu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_medtus': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'spec_id': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rss_post'", 'null': 'True', 'db_column': "'spec_id'", 'to': u"orm['medtus.Specialities']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('tinymce.models.HTMLField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rss']
