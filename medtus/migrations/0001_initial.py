# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Specialities'
        db.create_table(u'Specialities', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'medtus', ['Specialities'])

        # Adding model 'PostLinks'
        db.create_table(u'PostLinks', (
            ('post_id', self.gf('django.db.models.fields.IntegerField')(max_length=10, primary_key=True)),
            ('service_id', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal(u'medtus', ['PostLinks'])

        # Adding model 'Countries'
        db.create_table(u'Countries', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'medtus', ['Countries'])

        # Adding model 'Towns'
        db.create_table(u'Towns', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_id', self.gf('django.db.models.fields.IntegerField')()),
            ('region', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('checked', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'medtus', ['Towns'])

        # Adding model 'Statistics'
        db.create_table(u'statistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='id')),
            ('material_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('service_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('viewings', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('likes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'medtus', ['Statistics'])

        # Adding model 'Like'
        db.create_table(u'medtus_like', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('material_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('service_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.MyUser'])),
            ('createdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'medtus', ['Like'])

        # Adding model 'Visited'
        db.create_table(u'medtus_visited', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('material_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('counter', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'medtus', ['Visited'])

        # Adding model 'MaterialPhoto'
        db.create_table(u'medtus_materialphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='id')),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('service_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('thumb', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'medtus', ['MaterialPhoto'])

        # Adding model 'MaterialVideo'
        db.create_table(u'medtus_materialvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='id')),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('service_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('preview', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'medtus', ['MaterialVideo'])


    def backwards(self, orm):
        # Deleting model 'Specialities'
        db.delete_table(u'Specialities')

        # Deleting model 'PostLinks'
        db.delete_table(u'PostLinks')

        # Deleting model 'Countries'
        db.delete_table(u'Countries')

        # Deleting model 'Towns'
        db.delete_table(u'Towns')

        # Deleting model 'Statistics'
        db.delete_table(u'statistics')

        # Deleting model 'Like'
        db.delete_table(u'medtus_like')

        # Deleting model 'Visited'
        db.delete_table(u'medtus_visited')

        # Deleting model 'MaterialPhoto'
        db.delete_table(u'medtus_materialphoto')

        # Deleting model 'MaterialVideo'
        db.delete_table(u'medtus_materialvideo')


    models = {
        u'account.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'account.myuser': {
            'ICQ_Skype': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'MyUser'},
            'addexperience': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'addspeciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'myuser_addspeciality'", 'null': 'True', 'db_column': "'addspeciality'", 'to': u"orm['medtus.Specialities']"}),
            'addtitle': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Category']"}),
            'cathedra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medtus.Countries']", 'null': 'True', 'db_column': "'country'", 'blank': 'True'}),
            'createdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dissertation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'email_visible': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'faculty': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'graduate': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'graduate_year': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'lastaccess': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'lastvisit': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'pass'"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'phone_visible': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'social': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'spec_id': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'myuser_spec_id'", 'null': 'True', 'db_column': "'spec_id'", 'to': u"orm['medtus.Specialities']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medtus.Towns']", 'null': 'True', 'db_column': "'town'", 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'user_ptr_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'medtus.countries': {
            'Meta': {'object_name': 'Countries', 'db_table': "u'Countries'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'medtus.like': {
            'Meta': {'object_name': 'Like'},
            'createdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.MyUser']"})
        },
        u'medtus.materialphoto': {
            'Meta': {'object_name': 'MaterialPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'medtus.materialvideo': {
            'Meta': {'object_name': 'MaterialVideo'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preview': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'medtus.postlinks': {
            'Meta': {'object_name': 'PostLinks', 'db_table': "u'PostLinks'"},
            'object_id': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'post_id': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'}),
            'service_id': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        },
        u'medtus.specialities': {
            'Meta': {'object_name': 'Specialities', 'db_table': "u'Specialities'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'medtus.statistics': {
            'Meta': {'object_name': 'Statistics', 'db_table': "u'statistics'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'likes': ('django.db.models.fields.TextField', [], {}),
            'material_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'viewings': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'medtus.towns': {
            'Meta': {'object_name': 'Towns', 'db_table': "u'Towns'"},
            'checked': ('django.db.models.fields.IntegerField', [], {}),
            'country_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {})
        },
        u'medtus.visited': {
            'Meta': {'object_name': 'Visited'},
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['medtus']