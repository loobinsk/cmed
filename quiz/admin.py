# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from .models import Quiz, Category, SubCategory, Progress, Question, Essay_Question
from .models import MCQuestion, Answer, TF_Question
from account.models import MyUser
import json

class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = ['max_questions', 'answers_at_end', 'exam_paper', 'single_attempt']

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial =\
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set = self.cleaned_data['questions']
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('description', 'category', )


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('sub_category', )
    list_display = ('sub_category', 'category',)
    list_filter = ('category',)


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category',
              'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]


class ProgressAdminForm(forms.ModelForm):
    admin_answers = forms.CharField()

    class Meta:
        model = Progress
        fields = '__all__'




class ProgressAdmin(admin.ModelAdmin):

    #TODO: create a user section
    form = ProgressAdminForm


    list_display = ('user_id', 'user_fname', 'user_lname', 'user_surname', 'user_email', 'user_phone', 'user_spec_id',
                    'user_country', 'user_town', 'quiz_title', 'overallscore', 'score', 'answers')
    list_filter = ('test_id__post',)
    fields = 'overallscore', 'score', 'admin_answers'
    readonly_fields = 'overallscore', 'score', 'admin_answers'

    def admin_answers(self, obj):
        x=dict()
        z = json.loads(obj.answers)
        for k in z:
            y = Question.objects.get(id=k)
            try:
                mc = MCQuestion.objects.get(id=k)
                MCcheck=True
            except:
                MCcheck=False
                pass

            if MCcheck:
                zz = Answer.objects.get(id=z[k])
                x[str(y)] = str(zz)
            else:
                x[str(y)] = z[k]
        y=json.dumps(x).decode('unicode-escape').encode('utf8')
        return y

    admin_answers.short_description = "Ответы"


    def quiz_title(self, obj):
        return obj.test_id.title

    def user_fname(self, obj):
        return obj.user.firstname

    def user_lname(self, obj):
        return obj.user.lastname

    def user_surname(self, obj):
        return obj.user.surname

    def user_email(self, obj):
        if hasattr(obj.user, 'email'):
            return obj.user.email
        else:
            return ""

    def user_town(self, obj):
        if hasattr(obj.user, 'town'):
            return obj.user.town
        else:
            return ""

    def user_country(self, obj):
        if hasattr(obj.user, 'country'):
            return obj.user.country
        else:
            return ""

    def user_spec_id(self, obj):
        if hasattr(obj.user, 'spec_id'):
            return obj.user.spec_id
        else:
            return ""

    def user_phone(self, obj):
        if hasattr(obj.user, 'phone'):
            return obj.user.phone
        else:
            return ""

    def user_id(self, obj):
        return obj.user.id


class TFQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category',
              'figure', 'quiz', 'explanation', 'correct',)

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)


class EssayQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category', 'quiz', 'explanation', )
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(TF_Question, TFQuestionAdmin)
admin.site.register(Essay_Question, EssayQuestionAdmin)
