__author__ = 'PekopT'


def request(request):
    from cmedu import settings
    return {
        'global': settings.TEMPLATE_VARS,
        'global_formats': {
            'video': settings.VIDEO_FORMATS_LIST,
            'formats': settings.FORMATS_LIST,
            'post': settings.POST_FORMATS_LIST
        }
    }