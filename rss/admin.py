from django.contrib import admin
from django import forms
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from mce_filebrowser.admin import MCEFilebrowserAdmin

from comments.admin import CommentsAdminLink
from rss.models import Filters, Feeds, Posts
from medtus.models import Statistics
from account.mixins import StaffPermissionMixin


class RssAdminForm(forms.ModelForm):
    likes = forms.CharField(label='likes', required=False, widget=forms.Textarea)
    viewings = forms.IntegerField(label='viewings', required=False)

    def save(self, commit=True):
        instance = super(RssAdminForm, self).save(commit=False)
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
                stat, created = Statistics.objects.get_or_create(service_id=69, material_id=self.instance.id, defaults=defaults)
                if not created:
                    Statistics.objects.filter(service_id=69, material_id=self.instance.id).update(**defaults)
        return instance

    def __init__(self, *args, **kwargs):
        super(RssAdminForm, self).__init__(*args, **kwargs)

        stat = Statistics.objects.filter(service_id=69, material_id=self.instance.id).first()
        if stat:
            self.fields['likes'].initial = stat.likes
            self.fields['viewings'].initial = stat.viewings



class RssAdmin(StaffPermissionMixin, ForeignKeyAutocompleteAdmin, MCEFilebrowserAdmin, CommentsAdminLink):
    list_display = ('title', 'show', 'id', 'comments_link', 'format')
    search_fields = ('format',)
    form = RssAdminForm

    def queryset(self, request):
        return super(RssAdmin, self).queryset(request)


admin.site.register(Posts, RssAdmin)
admin.site.register(Filters)
admin.site.register(Feeds)
