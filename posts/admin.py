# -*- coding: utf-8 -*-
from xmlrpclib import escape

from django.contrib import admin
from django import forms
from mce_filebrowser.admin import MCEFilebrowserAdmin
from django.utils.safestring import mark_safe

from posts.models import Posts
from account.models import MyUser
from account.mixins import StaffPermissionMixin
from medtus.models import MaterialPhoto, MaterialVideo, Statistics
from comments.admin import CommentsAdminLink


ALL_TYPES = (
    ('1', 'Новость'),
    ('2', 'Статья'),
    ('3', 'Онлайн-трансляции'),
    ('4', 'Вопрос коллегам'),
    ('5', 'Частное мнение'),
    ('6', 'Книги и журналы'),
    ('7', 'Тренинги'),
    ('8', 'Резюме и вакансии'),
    ('9', 'Обсуждение препарата'),
    # ('10', ''),
    ('11', 'Опросы и исследования  Премия Доктор Года'),
    ('12', 'Клинический случай'),
    # ('15', ''),
    # ('50', ''),
    ('88', 'Мероприятия'),
    ('99', 'Видеоматериалы'),
)


def get_display_method(rddict, queryset, key):
    """Re-implementation of inspect.getmembers(rddict,inspect.ismethod) and
    a test to see if this is a get_field_status method.  Had to reimplement inspect
    because it was bombing on the object - expecting some property that is not present."""

    rdobj = queryset[0].__class__.objects.filter(resultdata_id=rddict["resultdata_id"]).get()
    targetname = "get_%s_display" % key
    display_func = False

    for name in dir(rdobj):
        if name == targetname:
            try:
                display_func = getattr(rdobj, name)
                break
            except Exception, e:
                pass

    return display_func


def result_as_table(queryset, fieldnames=None):
    """Take a resultdata queryset and return it as a HTML table.
    Columns will be returned in the order they are declared in the model.

    Optionally, provide a list of fieldnames, which will be used to limit the output."""

    dictlist = queryset.values()
    output = "<table>\n"
    output_keys = []

    if fieldnames:
        names = fieldnames
    else:
        names = dictlist.field_names

    for name in names:

        if not name.endswith("_id"):
            output_keys.append(name)
            output = "".join((output, "<th>%s</th>\n" % escape(name.replace("_", " ").capitalize())))

    for rddict in dictlist:

        output = "".join((output, "<tr>\n"))

        for key in output_keys:
            val = rddict[key]
            if not key.endswith("_id"):

                display_func = get_display_method(rddict, queryset, key)

                if display_func:
                    output = "".join((output, "<td>%s</td>\n" % escape(display_func())))
                else:
                    output = "".join((output, "<td>%s</td>\n" % escape(val)))

        output = "".join((output, "</tr>\n"))

    return mark_safe("".join((output, "</table>\n")))


result_as_table.is_safe = True


class ModelLinkWidget(forms.Widget):
    def __init__(self, obj, attrs=None, **kwargs):
        self.object = obj
        if kwargs.get('rel'):
            self.rel = kwargs.get('rel')
        super(ModelLinkWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if self.object.pk:
            model = self.rel

            rels = model.objects.filter(object_id=self.object.pk)
            if rels.exists():
                object = rels[0]
                img = object.preview if isinstance(object, MaterialVideo) else object.thumb
            else:
                return mark_safe(u'')

            return mark_safe(
                u'<a target="_blank" href="../../../%s/%s/%s/"><img src="%s" width="100"/></a>' %
                (
                    object._meta.app_label,
                    object._meta.object_name.lower(),
                    object.pk, img
                )
            )
        else:
            return mark_safe(u'')


class CommentsWidget(forms.Widget):
    def __init__(self, obj, *args, **kwargs):
        self.object = obj
        super(CommentsWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if self.object.pk:
            from django.template import loader, Context

            t = loader.get_template('posts/admin/comments_table.html')
            comments = [x[0] for x in self.object.treeComments()]
            c = Context({'comments': comments})
            return t.render(c)


class PostForm(forms.ModelForm):
    photo = forms.CharField(label='photo', required=False)
    video = forms.CharField(label='video', required=False)
    comments = forms.CharField(label='comments', required=False)
    likes = forms.CharField(label='likes', required=False, widget=forms.Textarea)
    viewings = forms.IntegerField(label='viewings', required=False)

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            defaults = {}
            if self.cleaned_data.get('likes'):
                defaults['likes'] = self.cleaned_data['likes']
            if self.cleaned_data.get('viewings') is not None:
                defaults['viewings'] = self.cleaned_data['viewings']
            elif defaults:
                defaults['viewings'] = 0
            if defaults:
                stat, created = Statistics.objects.get_or_create(service_id=18, material_id=self.instance.id, defaults=defaults)
                if not created:
                    Statistics.objects.filter(service_id=18, material_id=self.instance.id).update(**defaults)
        return instance

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if 'user_id' in self.initial:
            self.fields['user_id'].queryset = MyUser.objects.filter(pk=self.initial['user_id'])
        else:
            self.fields['user_id'].queryset = MyUser.objects.filter(pk=self.initial['user_id'])

        # instance is always available, it just does or doesn't have pk.
        self.fields['photo'].widget = ModelLinkWidget(self.instance, rel=MaterialPhoto)
        self.fields['video'].widget = ModelLinkWidget(self.instance, rel=MaterialVideo)
        self.fields['comments'].widget = CommentsWidget(self.instance)

        stat = Statistics.objects.filter(service_id=18, material_id=self.instance.id).first()
        if stat:
            self.fields['likes'].initial = stat.likes
            self.fields['viewings'].initial = stat.viewings


class PostTypeListFilter(admin.SimpleListFilter):
    title = "Тип поста"

    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return ((i[0], i[1].decode('UTF-8')) for i in ALL_TYPES)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())


class PostsAdmin(StaffPermissionMixin, MCEFilebrowserAdmin, CommentsAdminLink):
    list_display = ('id', 'comments_link', 'user_id', 'title', 'status', 'createdate', 'type_of_post')
    search_fields = ('id', 'title', 'status', 'anons', 'content')
    list_filter = (PostTypeListFilter,)
    form = PostForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "spec_id":
            from medtus.models import Specialities

            kwargs["queryset"] = Specialities.objects.order_by('name')
        return super(PostsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def type_of_post(self, obj):
        return dict(ALL_TYPES).get(str(obj.type), 'Неизвестный тип')


admin.site.register(Posts, PostsAdmin)
