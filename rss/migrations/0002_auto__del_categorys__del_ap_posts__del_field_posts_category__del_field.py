# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Categorys'
        db.delete_table(u'rss_categorys')

        # Deleting model 'Ap_Posts'
        db.delete_table(u'rss_ap_posts')

        # Deleting field 'Posts.category'
        db.delete_column(u'rss_posts', 'category_id')

        # Deleting field 'Posts.parsed'
        db.delete_column(u'rss_posts', 'parsed')

        # Adding field 'Posts.spec_id'
        db.add_column(u'rss_posts', 'spec_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rss_post', null=True, db_column='spec_id', to=orm['medtus.Specialities']),
                      keep_default=False)

        # Adding field 'Posts.createdate'
        db.add_column(u'rss_posts', 'createdate',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Posts.code'
        db.add_column(u'rss_posts', 'code',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Posts.status'
        db.add_column(u'rss_posts', 'status',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Posts.image'
        db.add_column(u'rss_posts', 'image',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Posts.updatedate'
        db.add_column(u'rss_posts', 'updatedate',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Posts.source'
        db.add_column(u'rss_posts', 'source',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Posts.format'
        db.add_column(u'rss_posts', 'format',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)

        # Adding field 'Posts.comment_cnt'
        db.add_column(u'rss_posts', 'comment_cnt',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Posts.comment_show'
        db.add_column(u'rss_posts', 'comment_show',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Posts.popular'
        db.add_column(u'rss_posts', 'popular',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Posts.show_cmedu'
        db.add_column(u'rss_posts', 'show_cmedu',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Posts.show_medtus'
        db.add_column(u'rss_posts', 'show_medtus',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Posts.public_main'
        db.add_column(u'rss_posts', 'public_main',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


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

        # Adding model 'Ap_Posts'
        db.create_table(u'rss_ap_posts', (
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('public_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('format', self.gf('django.db.models.fields.IntegerField')()),
            ('createdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('show_medtus', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment_cnt', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('popular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_cmedu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss.Posts'])),
            ('comment_show', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'rss', ['Ap_Posts'])

        # Adding field 'Posts.category'
        db.add_column(u'rss_posts', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['rss.Categorys']),
                      keep_default=False)

        # Adding field 'Posts.parsed'
        db.add_column(u'rss_posts', 'parsed',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=None, blank=True),
                      keep_default=False)

        # Deleting field 'Posts.spec_id'
        db.delete_column(u'rss_posts', 'spec_id')

        # Deleting field 'Posts.createdate'
        db.delete_column(u'rss_posts', 'createdate')

        # Deleting field 'Posts.code'
        db.delete_column(u'rss_posts', 'code')

        # Deleting field 'Posts.status'
        db.delete_column(u'rss_posts', 'status')

        # Deleting field 'Posts.image'
        db.delete_column(u'rss_posts', 'image')

        # Deleting field 'Posts.updatedate'
        db.delete_column(u'rss_posts', 'updatedate')

        # Deleting field 'Posts.source'
        db.delete_column(u'rss_posts', 'source')

        # Deleting field 'Posts.format'
        db.delete_column(u'rss_posts', 'format')

        # Deleting field 'Posts.comment_cnt'
        db.delete_column(u'rss_posts', 'comment_cnt')

        # Deleting field 'Posts.comment_show'
        db.delete_column(u'rss_posts', 'comment_show')

        # Deleting field 'Posts.popular'
        db.delete_column(u'rss_posts', 'popular')

        # Deleting field 'Posts.show_cmedu'
        db.delete_column(u'rss_posts', 'show_cmedu')

        # Deleting field 'Posts.show_medtus'
        db.delete_column(u'rss_posts', 'show_medtus')

        # Deleting field 'Posts.public_main'
        db.delete_column(u'rss_posts', 'public_main')


    models = {
        u'medtus.specialities': {
            'Meta': {'object_name': 'Specialities', 'db_table': "u'Specialities'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'passval': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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