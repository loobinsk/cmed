# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from mce_filebrowser.admin import MCEFilebrowserAdmin
from events.models import Events
from comments.admin import CommentsAdminLink
from medtus.models import Statistics
from account.mixins import StaffPermissionMixin


class EventAdminForm(forms.ModelForm):
    likes = forms.CharField(label='likes', required=False, widget=forms.Textarea)
    viewings = forms.IntegerField(label='viewings', required=False)

    def save(self, commit=True):
        instance = super(EventAdminForm, self).save(commit=False)
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
                stat, created = Statistics.objects.get_or_create(service_id=6, material_id=self.instance.id, defaults=defaults)
                if not created:
                    Statistics.objects.filter(service_id=6, material_id=self.instance.id).update(**defaults)
        return instance

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)

        stat = Statistics.objects.filter(service_id=6, material_id=self.instance.id).first()
        if stat:
            self.fields['likes'].initial = stat.likes
            self.fields['viewings'].initial = stat.viewings


class EventsAdmin(StaffPermissionMixin, ForeignKeyAutocompleteAdmin, MCEFilebrowserAdmin, CommentsAdminLink):
    list_display = ('id', 'comments_link','title', 'content', 'type_id')
    search_fields = ('id', 'title', 'content')
    raw_id_fields = ('user_id',)
    form = EventAdminForm

    def queryset(self, request):
        return super(EventsAdmin, self).queryset(request).filter(type_id__in=(1, 2, 3, 5, 6, 11))


admin.site.register(Events, EventsAdmin)