import os
import urllib

from django.contrib import admin
#from mce_filebrowser.admin import MCEFilebrowserAdmin
from django.conf import settings

from medtus.models import MaterialVideo, PrivateContentPageUsers, MaterialPhoto, Translation, Feedback, Specialities, Towns, ContentPage, \
    TranslationVisit, TranslationViewer, TranslationModal
from cuter.cuter import resize_and_crop
from lenta.views import do_URL
from account.mixins import CSVTruncateAdmin


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'picture', 'thumb')
    exclude = ('thumb',)

    def save_model(self, request, obj, form, change):
        obj.save()
        from fileshandle.views import size

        file_path = obj.picture.name.split('/')

        path = os.path.join(settings.MEDIA_ROOT, file_path[0])
        url = os.path.join(settings.MEDIA_URL, file_path[0])
        url1 = os.path.join('/media/post_images/', file_path[1])
        infile = file_path[1]

        outfile = os.path.join(path, u'thumb_{0}'.format(infile))

        resize_and_crop(u'{0}/{1}'.format(path, infile), outfile, size)
        output_url = os.path.join(url, u'thumb_{0}'.format(infile))
        obj.picture = url1
        obj.thumb = output_url

        obj.save()


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'data', 'preview')

    exclude = ('preview',)

    def save_model(self, request, obj, form, change):
        obj.save()

        video_url = obj.data
        try:
            try:
                urllib.urlopen(video_url)
                address = do_URL(video_url)
                if 'v' not in address:
                    raise VideoAdminException
                address = address['v']
            except:
                address = video_url

            URL = "https://img.youtube.com/vi/{0}/0.jpg".format(address)
            INFO_URL = "https://youtube.com/get_video_info?video_id={0}".format(address)

            obj.data = '<iframe width="430" height="315" src="//www.youtube.com/embed/{0}" frameborder="0" allowfullscreen></iframe>'.format(
                address)

            urllib.urlopen(INFO_URL)

            path = os.path.join(settings.MEDIA_ROOT, 'post_images')

            if not os.path.exists(path):
                os.makedirs(path)

            output_file = os.path.join(path, u'{0}.jpg'.format(address))

            resource = urllib.urlopen(URL)
            output = open(output_file, "wb+")
            output.write(resource.read())
            output.close()
            output_url = os.path.join(settings.MEDIA_URL, 'post_images', u'{0}.jpg'.format(address))

            obj.preview = output_url

        except VideoAdminException:
            obj.data = ''

        obj.save()


class TranslationModalAdminInline(admin.StackedInline):
    model = TranslationModal
    extra = 1
    fields = ['datetime']

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link', 'active')
    inlines = [TranslationModalAdminInline]

class TranslationModalAdmin(admin.ModelAdmin):
    list_display = ('translation', 'datetime')

class TranslationViewerAdmin(CSVTruncateAdmin):
    list_display = ('id', 'post', 'user', 'checks_counter')
    list_filter = ('post', 'checks_counter')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'position', 'topic', 'text', 'answered', 'datetime')
    list_filter = ('answered',)


class VideoAdminException(Exception):
    pass


from django import forms
class CabModelForm( forms.ModelForm ):
    words = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Specialities
        fields = '__all__'

class SpecAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title')
    form = CabModelForm

class TownAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_id', 'region', 'name')
    search_fields = ('name', )

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("size", "okrug", "checked", )
        form = super(TownAdmin, self).get_form(request, obj, **kwargs)
        return form



class ContentPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_alias')
    # def has_add_permission(self, request):
    #     return not ContentPage.objects.exists()

class PrivateContentPageUsersAdmin(CSVTruncateAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'speciality', 'city', 'page', 'dt_create')
    list_filter = ('page',)
    list_per_page = 100
    csv_record_limit = 200000

class TranslationVisitAdmin(admin.ModelAdmin):
    list_display = ('dt_create', 'dt_update', 'post', 'user')
    readonly_fields = ('dt_create', 'dt_update', 'post', 'user')


admin.site.register(MaterialVideo, VideoAdmin)
admin.site.register(MaterialPhoto, PhotoAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(TranslationModal, TranslationModalAdmin)
admin.site.register(Specialities, SpecAdmin)
admin.site.register(Towns, TownAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(ContentPage, ContentPageAdmin)
admin.site.register(PrivateContentPageUsers, PrivateContentPageUsersAdmin)
admin.site.register(TranslationVisit, TranslationVisitAdmin)
admin.site.register(TranslationViewer, TranslationViewerAdmin)