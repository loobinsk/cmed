# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Filters'
        db.create_table('rss_filters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('words', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('passval', self.gf('django.db.models.fields.IntegerField')(default=30)),
        ))
        db.send_create_signal(u'rss', ['Filters'])

        # Adding model 'Feeds'
        db.create_table('rss_feeds', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'rss', ['Feeds'])

        # Adding M2M table for field filters on 'Feeds'
        m2m_table_name = db.shorten_name('rss_feeds_filters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feeds', models.ForeignKey(orm[u'rss.feeds'], null=False)),
            ('filters', models.ForeignKey(orm[u'rss.filters'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feeds_id', 'filters_id'])

        # Adding model 'Posts'
        db.create_table(u'rss_posts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss.Feeds'])),
            ('spec_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rss_post', null=True, db_column='spec_id', to=orm['medtus.Specialities'])),
            ('published', self.gf('django.db.models.fields.DateTimeField')()),
            ('createdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('text', self.gf('tinymce.models.HTMLField')(max_length=250)),
            ('href', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('format', self.gf('django.db.models.fields.IntegerField')()),
            ('comment_cnt', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment_show', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('popular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_cmedu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_medtus', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('public_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'rss', ['Posts'])


    def backwards(self, orm):
        # Deleting model 'Filters'
        db.delete_table('rss_filters')

        # Deleting model 'Feeds'
        db.delete_table('rss_feeds')

        # Removing M2M table for field filters on 'Feeds'
        db.delete_table(db.shorten_name('rss_feeds_filters'))

        # Deleting model 'Posts'
        db.delete_table(u'rss_posts')


    models = {
        u'medtus.specialities': {
            'Meta': {'object_name': 'Specialities', 'db_table': "u'Specialities'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'passval': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'words': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'rss.feeds': {
            'Meta': {'object_name': 'Feeds'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['rss.Filters']", 'null': 'True', 'blank': 'True'}),
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