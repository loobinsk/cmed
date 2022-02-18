# -*- coding: utf-8 -*-
from django.contrib import admin
import datetime
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.translation import ugettext_lazy as _

from account.models import MyUser, Timer, AllMsg
from account.mixins import CSVTruncateAdmin
from quiz.models import Quiz, Progress
from medtus.models import TranslationVisit
from posts.models import Posts

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class TestProgress(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = u'Результаты тестов:'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'score'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('pass', u'Тест пройден'),
            ('fail', u'Тест не пройден'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        filt=False
        passm=75
        test=0
        try:
            test=int(request.GET.get('post__id__exact'))
            filt=True
            try:
                q=Quiz.objects.get(post=test)
                passm=int(q.pass_mark)
            except:
                pass
        except:
            pass

        if filt:
            if self.value() == 'pass':
                return queryset.filter(user__progress__overallscore__gte=passm,user__progress__test_id__post=test)
            if self.value() == 'fail':
                return queryset.filter(user__progress__overallscore__lt=passm,user__progress__test_id__post=test)

        return queryset


class TimerAdmin(CSVTruncateAdmin):
    list_display = ('id', 'user_id', 'user', 'post_title', 'timer',
                    'user_lname', 'user_fname', 'user_surname', 'user_town',
                    'user_country', 'user_spec_id', 'user_graduate', 'time_join', 'time_leave', 'finish_time', 'test_score', 'user_organization')
    search_fields = ('user__firstname', 'user__lastname', 'user__surname', 'user__email', 'post__title')
    raw_id_fields = ('user',)
    list_filter = (('post',custom_titled_filter('Трансляция:')), TestProgress,)


    def test_score(self, obj):
        quiz = Quiz.objects.filter(post=obj.post).first()
        progress=Progress.objects.filter(test_id=quiz, user=obj.user).first()
        if progress:
         # return u"Тест пройден"
          return progress.overallscore
        return u"Нет результатов"

    def finish_time(self, obj):
        quiz = Quiz.objects.filter(post=obj.post).first()
        progress=Progress.objects.filter(test_id=quiz, user=obj.user).first()
        if progress:
          return progress.finish_time
        return u"Тест не пройден"

    test_score.short_description = 'Результаты тестов'
    finish_time.short_description = 'Время завершения теста'

    def post_title(self, obj):
        return obj.post.title

    def user_fname(self, obj):
        return obj.user.firstname

    def user_lname(self, obj):
        return obj.user.lastname

    def user_surname(self, obj):
        return obj.user.surname

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

    def user_graduate(self, obj):
        if hasattr(obj.user, 'graduate'):
            return obj.user.graduate
        else:
            return ""

    def user_organization(self, obj):
        if hasattr(obj.user, 'organization'):
            return obj.user.organization
        else:
            return ""        

    def user_id(self, obj):
        return obj.user.id

    def timer(self, obj):
        return str(datetime.timedelta(seconds=obj.time))

    def queryset(self, request):
        queryset = super(TimerAdmin, self).queryset(request).order_by('post', 'user')
        return queryset

    def time_join(self, obj):
        first_visit = TranslationVisit.objects.filter(post=obj.post, user=obj.user).order_by('-dt_update').first()
        return first_visit.dt_create if first_visit else ''
    time_join.short_description = "Time join"

    def time_leave(self, obj):
        last_visit = TranslationVisit.objects.filter(post=obj.post, user=obj.user).order_by('-dt_update').first()
        if last_visit and last_visit.dt_update:
            if last_visit.dt_update <= timezone.now() - datetime.timedelta(minutes=3):
                return last_visit.dt_update
            else:
                return 'online'
        else:
            return ''
    time_leave.short_description = 'Time leave'


class MyUserAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = MyUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserAdminForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]



class MyAdminPasswordChangeForm(AdminPasswordChangeForm):
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            else:
                import re
                p = re.compile(ur'[a-z\d]+', re.UNICODE | re.IGNORECASE)
                if not re.search(p, password1):
                    raise forms.ValidationError(u'В пароле доступны только символы A-Z и 0-9')
        return password2


# class MyUserAdmin(UserAdmin):
class MyUserAdmin(CSVTruncateAdmin, UserAdmin):
    form = MyUserAdminForm
    change_password_form = MyAdminPasswordChangeForm
    list_display = ('id', 'login', 'email', 'firstname', 'lastname', 'surname', 'phone_number', 'town', 'country',
                    'graduate', 'spec_id', 'createdate')
    list_filter = ('town', 'spec_id', 'graduate', 'country')
    search_fields = ('firstname', 'lastname', 'surname', 'email',
                     'town__name', 'spec_id__name', 'graduate__name', 'country__name')
    list_per_page = 100

    csv_record_limit = 200000

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('login', 'firstname', 'lastname', 'surname')}),
        (_('Info'), {'fields': ('avatar', 'sex', 'birthday', 'spec_id',
                                'experience', 'addspeciality', 'addexperience',
                                'graduate', 'dissertation', 'title', 'addtitle', 'category', 'organization',
                                'job', 'site', 'school', 'graduate_year', 'faculty', 'cathedra', 'country',
                                'town', 'phone_number', 'phone_visible', 'email_visible', 'ICQ_Skype', 'social',
                                'status', 'awords'
                                )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('lastaccess', 'lastvisit')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'email', 'password1', 'password2')}
         ),
    )
    ordering = ('id',)

    def firstname(self, obj):
        return obj.firstname

    def lastname(self, obj):
        return obj.lastname

    def surname(self, obj):
        return obj.surname

    def email(self, obj):
        return obj.email

    def login(self, obj):
        return obj.login


class AllMsgAdmin(admin.ModelAdmin):
    list_display = ('id', 'msgs', 'datetime', 'unreaded')
    list_filter = ('id', 'msgs', 'datetime', 'unreaded')
admin.site.register(AllMsg, AllMsgAdmin)

admin.site.register(Timer, TimerAdmin)
admin.site.register(MyUser, MyUserAdmin)
