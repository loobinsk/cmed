# -*- coding: utf-8 -*-
"""
Django settings for cmedu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(SETTINGS_DIR, os.pardir))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@=6=2e@!f-vj&o*@u97#tgm0q$(ftxu(85=n*2-6vygardy%-y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
        'localhost', '127.0.0.1', 'www.vrvm.ru', 'vrvm.ru',
        'vrachivmeste.ru', 'www.vrachivmeste.ru', '45.80.69.219'
    ]

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'django_crontab',
    'django_extensions',
    'tinymce',
    'sorl.thumbnail',
    'settings',
    'simplejson',
    'library',
    'account',
    'lenta',
    'post',
    'medtus',
    'videos',
    'events',
    'posts',
    'records',
    'groups',
    'groups_posts',
    'comments',
    'lichnie',
    'cuter',
    'circle',
    'fileshandle',
    'partners',
    'photos',
    'banners',
    'rss',
    'lecturers',
    'quiz'
)

AUTHENTICATION_BACKENDS = (
    'cmedu.auth_backends.CustomUserModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

CUSTOM_USER_MODEL = 'account.MyUser'

PASSWORD_HASHERS = (
    'cmedu.mysql_hasher.MySQLHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cmedu.onlinenow.OnlineNowMiddleware',
]

ROOT_URLCONF = 'cmedu.urls'

WSGI_APPLICATION = 'cmedu.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6'USER': 'medtusdj_user',

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'medtusdj',
        'USER': 'medtusdj_user',
        'PASSWORD': 'Papa$$w0w0rd',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': "SET foreign_key_checks = 0;",
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATICFILES_FINDERS = [
#   'dajaxice.finders.DajaxiceFinder',
#     'compressor.finders.CompressorFinder',
# ]


MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/vrachivmeste.ru/medtus.djangohost.name/media'

PUBLIC_HTML_ROOT = '/var/www/vrachivmeste.ru/medtus.djangohost.name'

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/vrachivmeste.ru/medtus.djangohost.name/static'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static/'),
)

FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''


AUTH_USER_MODEL = 'account.MyUser'

LOGIN_URL = '/account/login'


ADMIN_EMAIL = 'vrvm.redaktor@gmail.com'
COORD_EMAIL = 'vrvm.koordinator@gmail.com'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'vrvm.ru@gmail.com'
EMAIL_HOST_PASSWORD = 'KAG2e{bTp?'


AVATAR_SIZE = 200, 200
SITE_URL = 'vrachivmeste.ru'


TINYMCE_JS_URL = os.path.join(SITE_URL, '/static/tiny_mce/tiny_mce_src.js')
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, "tiny_mce")
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins': 'autolink,lists,spellchecker,pagebreak,style,layer,table,save,'
               'advhr,advimage,advlink,emotions,iespell,inlinepopups,'
               'insertdatetime,preview,media,searchreplace,print,contextmenu,'
               'paste,directionality,fullscreen,noneditable,visualchars,'
               'nonbreaking,xhtmlxtras,template',
    'theme_advanced_buttons1': 'bold,italic,underline,strikethrough,|,'
                               'justifyleft,justifycenter,justifyright,'
                               'justifyfull,|,styleselect,formatselect,'
                               'fontsizeselect',
    'theme_advanced_buttons2': 'cut,copy,paste,pastetext,pasteword,|,search,'
                               'replace,|,bullist,numlist,|,outdent,indent,'
                               'blockquote,|,undo,redo,|,link,unlink,anchor,'
                               'image,cleanup,help,code,|,insertdate,'
                               'inserttime,preview,|,forecolor,backcolor',
    'theme_advanced_buttons3': 'tablecontrols,|,hr,removeformat,visualaid,|,'
                               'sub,sup,|,charmap,emotions,iespell,media,'
                               'advhr,|,print,|,ltr,rtl,|,fullscreen',
    'theme_advanced_buttons4': 'insertlayer,moveforward,movebackward,absolute,'
                               '|,styleprops,spellchecker,|,cite,abbr,acronym,'
                               'del,ins,attribs,|,visualchars,nonbreaking,'
                               'template,blockquote,pagebreak,|,insertfile,'
                               'insertimage',
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_resizing': True,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'file_browser_callback': 'mce_filebrowser',
    'width': 335,
    'relative_urls': False,
    'convert_urls': False,
    'extended_valid_elements': 'iframe[src|title|width|height|allowfullscreen|'
                               'frameborder]',
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

# TEMPLATE_CONTEXT_PROCESSORS += (
#    'django.core.context_processors.request',
#    'cmedu.context_processors.request',
# )

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_PATH],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # "account.context_processors.account",
                "cmedu.context_processors.request",
                "django.template.context_processors.request"
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '.logs/_logging_main.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '.logs/_logging_main_debug.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}

FORMATS_LIST = dict([
    (u'', u'Тип мероприятия'),
    (1, u'Вебинар'),
    (2, u'Конференция'),
    (3, u'Симпозиум'),
    # (4, u'Презентация'),
    (5, u'Семинар'),
    (6, u'Онлайн-трансляция'),
    (11, u'Выставка'),
    # (8, u'Эксклюзивные интервью'),
    # (9, u'Лекции'),
    # (10, u'Мероприятие')
])

VIDEO_FORMATS_LIST = dict([
    (u'', u'Тип видеоматериала'),
    (1, u'Медицинская анимация'),
    (2, u'Конференция'),
    (3, u'Телевизор'),
    (4, u'Хирургическая операция'),
    (5, u'Вебинар'),
    (6, u'Онлайн-трансляция'),
    (7, u'Эксклюзивное интервью'),
])

POST_FORMATS_LIST = dict([
    (u'', u'Тип материала'),
    (1, u'Новости'),
    (2, u'Статьи'),
    (3, u'Онлайн-трансляция'),
    (4, u'Вопрос коллегам'),
    (5, u'Частное мнение'),
    (6, u'Книги и журналы'),
    (7, u'Тренинги'),
    (8, u'Резюме и вакансии'),
    (9, u'Обсуждение препарата'),
    (11, u'Опросы и исследования'),
    (13, u'Опросы и исследования'),
    (12, u'Клинический случай'),
    (15, u'Публикации в группе'),
    (50, u'Партнёры')
])

TEMPLATE_VARS = {
    'placeholder_answer': u"Для того, чтобы ответить, напишите здесь что-нибудь",
    'placeholder_comment': u"Для того, чтобы оставить отзыв, напишите здесь что-нибудь"
}

DEFAULT_FROM_EMAIL = 'Врачи Вместе <noreply@vrvm.ru>'

RSS_PASS_DEFAULT, RSS_CATEGORY_DEFAULT = 30, 30


CRONJOBS = [
    ('30 2 * * *', 'django.core.management.call_command', ['boost_views']),
]


# file with local settings
try:
    from local_settings import *
except ImportError:
    pass
