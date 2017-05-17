import logging

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.contrib.auth.hashers import check_password


logger = logging.getLogger(__name__)


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            # user = self.user_class.objects.select_related().get(email=username)
            user = self.user_class.objects.get(email=username)
            pwd2 = 'mysqlsha1_sha1$%s' % user.password
            if check_password(password.encode('utf-8'), pwd2):
                return user

        except self.user_class.DoesNotExist, e:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
        if not self._user_class:
            raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class
