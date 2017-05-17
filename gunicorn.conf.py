bind = '127.0.0.1:8045'
workers = 3
user = "meddjango"
reload = True

try:
    from local_gunicorn import *
except ImportError:
    pass
