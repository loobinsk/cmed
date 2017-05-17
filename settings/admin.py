# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from django.core.urlresolvers import reverse

from settings.models import Settings, SocialIcons


class LinkWidget(forms.Widget):
    def __init__(self, obj, attrs=None):
        self.object = obj
        super(LinkWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if self.object.translation:
            url = reverse('detailtranslation', kwargs={'pk': self.object.translation.pk})
            return mark_safe(u'<a target="_blank" href="{url}" target="_blank">{url}</a>'.format(url=url))
        else:
            return mark_safe(u'')


class SettingsForm(forms.ModelForm):
    link = forms.CharField(label=u'Ссылка на трансляцию', required=False)

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['link'].widget = LinkWidget(self.instance)


class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm

admin.site.register(Settings, SettingsAdmin)
admin.site.register(SocialIcons)