# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'account_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Category'])

        # Adding model 'MyUser'
        db.create_table(u'account_myuser', (
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, db_column='pass')),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('avatar', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(max_length=256, null=True, blank=True)),
            ('spec_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='myuser_spec_id', null=True, db_column='spec_id', to=orm['medtus.Specialities'])),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('addspeciality', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='myuser_addspeciality', null=True, db_column='addspeciality', to=orm['medtus.Specialities'])),
            ('addexperience', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('graduate', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('dissertation', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('addtitle', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Category'])),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('job', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('graduate_year', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('faculty', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('cathedra', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medtus.Countries'], null=True, db_column='country', blank=True)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medtus.Towns'], null=True, db_column='town', blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('phone_visible', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('email_visible', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('ICQ_Skype', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('social', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('createdate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updatedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lastvisit', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lastaccess', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user_ptr_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='id')),
        ))
        db.send_create_signal(u'account', ['MyUser'])

        # Adding M2M table for field groups on 'MyUser'
        m2m_table_name = db.shorten_name(u'account_myuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'account.myuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'MyUser'
        m2m_table_name = db.shorten_name(u'account_myuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('myuser', models.ForeignKey(orm[u'account.myuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['myuser_id', 'permission_id'])

        # Adding model 'AdditionalImage'
        db.create_table(u'account_additionalimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'account', ['AdditionalImage'])

        # Adding model 'Aword'
        db.create_table(u'account_aword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.MyUser'])),
        ))
        db.send_create_signal(u'account', ['Aword'])

        # Adding model 'Timer'
        db.create_table(u'account_timer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.MyUser'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Posts'])),
            ('time', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'account', ['Timer'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'account_category')

        # Deleting model 'MyUser'
        db.delete_table(u'account_myuser')

        # Removing M2M table for field groups on 'MyUser'
        db.delete_table(db.shorten_name(u'account_myuser_groups'))

        # Removing M2M table for field user_permissions on 'MyUser'
        db.delete_table(db.shorten_name(u'account_myuser_user_permissions'))

        # Deleting model 'AdditionalImage'
        db.delete_table(u'account_additionalimage')

        # Deleting model 'Aword'
        db.delete_table(u'account_aword')

        # Deleting model 'Timer'
        db.delete_table(u'account_timer')


    models = {
        u'account.additionalimage': {
            'Meta': {'object_name': 'AdditionalImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'account.aword': {
            'Meta': {'object_name': 'Aword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.MyUser']"})
        },
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
        u'account.timer': {
            'Meta': {'object_name': 'Timer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Posts']"}),
            'time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.MyUser']"})
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
        u'medtus.specialities': {
            'Meta': {'object_name': 'Specialities', 'db_table': "u'Specialities'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'posts.posts': {
            'Meta': {'object_name': 'Posts', 'db_table': "u'Posts'"},
            'anons': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment_cnt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('tinymce.models.HTMLField', [], {}),
            'createdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'popular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spec_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medtus.Specialities']", 'null': 'True', 'db_column': "'spec_id'", 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'updatedate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.MyUser']", 'db_column': "'user_id'"})
        }
    }

    complete_apps = ['account']