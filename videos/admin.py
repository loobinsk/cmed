# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django_extensions.admin import ForeignKeyAutocompleteAdmin
#from mce_filebrowser.admin import MCEFilebrowserAdmin

from videos.models import Videos, VideoStatistics
from medtus.models import Statistics
from comments.admin import CommentsAdminLink
from account.mixins import StaffPermissionMixin

from django.contrib.admin import SimpleListFilter
from account.mixins import CSVTruncateAdmin

# admin.py
class VideoFilter(SimpleListFilter):
    title = 'video' # or use _('country') for translated title
    parameter_name = 'video'

    def lookups(self, request, model_admin):
        videos = set([c.video for c in model_admin.model.objects.all()])
        return [(c.id, c.title) for c in videos]
        # You can also use hardcoded model name like "Country" instead of 
        # "model_admin.model" if this is not direct foreign key filter

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(video__id__exact=self.value())
        else:
            return queryset


class VideosAdminForm(forms.ModelForm):
    likes = forms.CharField(label='likes', required=False, widget=forms.Textarea)
    viewings = forms.IntegerField(label='viewings', required=False)

    def save(self, commit=True):
        instance = super(VideosAdminForm, self).save(commit=False)
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
                stat, created = Statistics.objects.get_or_create(service_id=10, material_id=self.instance.id, defaults=defaults)
                if not created:
                    Statistics.objects.filter(service_id=10, material_id=self.instance.id).update(**defaults)
        return instance

    def __init__(self, *args, **kwargs):
        super(VideosAdminForm, self).__init__(*args, **kwargs)

        stat = Statistics.objects.filter(service_id=10, material_id=self.instance.id).first()
        if stat:
            self.fields['likes'].initial = stat.likes
            self.fields['viewings'].initial = stat.viewings


class VideosAdmin(StaffPermissionMixin, ForeignKeyAutocompleteAdmin, CommentsAdminLink):
    list_display = ('id', 'comments_link', 'title', 'description', 'format')
    search_fields = ('title', 'description', 'format')
    raw_id_fields = ('user_id',)
    form = VideosAdminForm

    def queryset(self, request):
        return super(VideosAdmin, self).queryset(request)

    readonly_fields = ['extended_statistic']

    def extended_statistic(self, obj):
        return '<a href="/admin/videos/videostatistics/?video={}">Перейти к подробной статистике</a>'.format(obj.pk)  # however you generate the link
    extended_statistic.allow_tags = True    

class VideoStatisticsAdmin(CSVTruncateAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'get_user_town', 'get_user_spec')
    list_filter = (VideoFilter,)
    raw_id_fields = ("user","video")
    csv_record_limit = 200000
    list_per_page = 400

    def get_user_town(self, obj):
        if hasattr(obj.user, 'town'):
            return obj.user.town
        else:
            return ""
    get_user_town.short_description = 'City'
    
        
    def get_user_spec(self, obj):
        if hasattr(obj.user, 'spec_id'):
            return obj.user.spec_id
        else:
            return ""        
    get_user_spec.short_description = 'Spec'    
    


admin.site.register(Videos, VideosAdmin)
admin.site.register(VideoStatistics, VideoStatisticsAdmin)
