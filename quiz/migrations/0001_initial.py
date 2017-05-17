# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'quiz_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'quiz', ['Category'])

        # Adding model 'SubCategory'
        db.create_table(u'quiz_subcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_category', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'quiz', ['SubCategory'])

        # Adding model 'Quiz'
        db.create_table(u'quiz_quiz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.SlugField')(max_length=60)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Category'], null=True, blank=True)),
            ('random_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('max_questions', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('answers_at_end', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_paper', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('single_attempt', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pass_mark', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('success_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fail_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medtus.Translation'], null=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'quiz', ['Quiz'])

        # Adding model 'Progress'
        db.create_table(u'quiz_progress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.MyUser'])),
            ('score', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('overallscore', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('answers', self.gf('django.db.models.fields.TextField')(default=u'{}', blank=True)),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
        ))
        db.send_create_signal(u'quiz', ['Progress'])

        # Adding model 'Sitting'
        db.create_table(u'quiz_sitting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.MyUser'])),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
            ('question_order', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024)),
            ('question_list', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024)),
            ('incorrect_questions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024, blank=True)),
            ('current_score', self.gf('django.db.models.fields.IntegerField')()),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_answers', self.gf('django.db.models.fields.TextField')(default=u'{}', blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'quiz', ['Sitting'])

        # Adding model 'Question'
        db.create_table(u'quiz_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Category'], null=True, blank=True)),
            ('sub_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.SubCategory'], null=True, blank=True)),
            ('figure', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('explanation', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal(u'quiz', ['Question'])

        # Adding M2M table for field quiz on 'Question'
        m2m_table_name = db.shorten_name(u'quiz_question_quiz')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'quiz.question'], null=False)),
            ('quiz', models.ForeignKey(orm[u'quiz.quiz'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'quiz_id'])

        # Adding model 'Essay_Question'
        db.create_table(u'quiz_essay_question', (
            (u'question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quiz.Question'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'quiz', ['Essay_Question'])

        # Adding model 'MCQuestion'
        db.create_table(u'quiz_mcquestion', (
            (u'question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quiz.Question'], unique=True, primary_key=True)),
            ('answer_order', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'quiz', ['MCQuestion'])

        # Adding model 'Answer'
        db.create_table(u'quiz_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.MCQuestion'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'quiz', ['Answer'])

        # Adding model 'TF_Question'
        db.create_table(u'quiz_tf_question', (
            (u'question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quiz.Question'], unique=True, primary_key=True)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'quiz', ['TF_Question'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'quiz_category')

        # Deleting model 'SubCategory'
        db.delete_table(u'quiz_subcategory')

        # Deleting model 'Quiz'
        db.delete_table(u'quiz_quiz')

        # Deleting model 'Progress'
        db.delete_table(u'quiz_progress')

        # Deleting model 'Sitting'
        db.delete_table(u'quiz_sitting')

        # Deleting model 'Question'
        db.delete_table(u'quiz_question')

        # Removing M2M table for field quiz on 'Question'
        db.delete_table(db.shorten_name(u'quiz_question_quiz'))

        # Deleting model 'Essay_Question'
        db.delete_table(u'quiz_essay_question')

        # Deleting model 'MCQuestion'
        db.delete_table(u'quiz_mcquestion')

        # Deleting model 'Answer'
        db.delete_table(u'quiz_answer')

        # Deleting model 'TF_Question'
        db.delete_table(u'quiz_tf_question')


    models = {
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
            'Meta': {'object_name': 'MyUser', 'index_together': "[['id', 'town'], ['id', 'spec_id']]"},
            'addexperience': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'addspeciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'myuser_addspeciality'", 'null': 'True', 'db_column': "'addspeciality'", 'to': u"orm['medtus.Specialities']"}),
            'addtitle': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'awords': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Aword']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Category']", 'null': 'True', 'blank': 'True'}),
            'cathedra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medtus.Countries']", 'null': 'True', 'db_column': "'country'", 'blank': 'True'}),
            'createdate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dissertation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'email_visible': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'faculty': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'graduate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Graduate']", 'null': 'True', 'blank': 'True'}),
            'graduate_year': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'lastaccess': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'lastvisit': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_column': "'pass'", 'blank': 'True'}),
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
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
        u'library.graduate': {
            'Meta': {'object_name': 'Graduate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
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
            'passval': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'words': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'medtus.towns': {
            'Meta': {'unique_together': "(['country_id', 'region', 'name'],)", 'object_name': 'Towns', 'db_table': "u'Towns'", 'index_together': "[['country_id', 'name']]"},
            'checked': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'country_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        u'medtus.translation': {
            'Meta': {'object_name': 'Translation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data': ('tinymce.models.HTMLField', [], {'default': 'None', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u0422\\u0440\\u0430\\u043d\\u0441\\u043b\\u044f\\u0446\\u0438\\u044f'", 'max_length': '255'})
        },
        u'quiz.answer': {
            'Meta': {'object_name': 'Answer'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.MCQuestion']"})
        },
        u'quiz.category': {
            'Meta': {'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'quiz.essay_question': {
            'Meta': {'ordering': "[u'category']", 'object_name': 'Essay_Question', '_ormbases': [u'quiz.Question']},
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['quiz.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'quiz.mcquestion': {
            'Meta': {'ordering': "[u'category']", 'object_name': 'MCQuestion', '_ormbases': [u'quiz.Question']},
            'answer_order': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['quiz.Question']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'quiz.progress': {
            'Meta': {'object_name': 'Progress'},
            'answers': ('django.db.models.fields.TextField', [], {'default': "u'{}'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overallscore': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'score': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Quiz']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.MyUser']"})
        },
        u'quiz.question': {
            'Meta': {'ordering': "[u'category']", 'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Category']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'explanation': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'figure': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['quiz.Quiz']", 'symmetrical': 'False', 'blank': 'True'}),
            'sub_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.SubCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'answers_at_end': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Category']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exam_paper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fail_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_questions': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pass_mark': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medtus.Translation']", 'null': 'True', 'blank': 'True'}),
            'random_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'single_attempt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '60'})
        },
        u'quiz.sitting': {
            'Meta': {'object_name': 'Sitting'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_score': ('django.db.models.fields.IntegerField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incorrect_questions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024', 'blank': 'True'}),
            'question_list': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024'}),
            'question_order': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Quiz']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.MyUser']"}),
            'user_answers': ('django.db.models.fields.TextField', [], {'default': "u'{}'", 'blank': 'True'})
        },
        u'quiz.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Category']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_category': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'quiz.tf_question': {
            'Meta': {'ordering': "[u'category']", 'object_name': 'TF_Question', '_ormbases': [u'quiz.Question']},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['quiz.Question']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['quiz']