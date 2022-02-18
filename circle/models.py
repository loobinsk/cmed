from django.db import models
from django.db.models import Q

from account.models import MyUser


# Create your models here.

class Circle(models.Model):
    parent = models.ForeignKey(MyUser, related_name='circle_parent')
    friend = models.ForeignKey(MyUser, related_name='circle_friend')
    activated = models.BooleanField(default=False)
    createdate = models.DateTimeField(auto_now_add=True)


class Dialog(models.Model):
    authA = models.ForeignKey(MyUser, related_name='dialog_authA')
    authB = models.ForeignKey(MyUser, related_name='dialog_authB')

    auth_a_deleted = models.BooleanField(default=0)
    auth_b_deleted = models.BooleanField(default=0)

    createdate = models.DateTimeField(auto_now_add=True)

    def calclastrecord(self):
        try:
            q1 = Q(auth=self.authA, dialog=self)
            q2 = Q(auth=self.authB, dialog=self)
            return Record.objects.filter(q1 | q2).order_by('createdate').last()
        except Exception:
            return ''

    def calccountrecord(self):
        q1 = Q(auth=self.authA, dialog=self)
        q2 = Q(auth=self.authB, dialog=self)
        return Record.objects.filter(q1 | q2).count()

    lastrecord = property(calclastrecord)
    countrecords = property(calccountrecord)


class Record(models.Model):
    auth = models.ForeignKey(MyUser, related_name='record_auth')
    value = models.CharField(max_length=2048, blank=True, null=True)
    dialog = models.ForeignKey(Dialog)
    createdate = models.DateTimeField(auto_now_add=True)
    viewed = models.DateTimeField(blank=True)
    moderated = models.BooleanField(False)
    count = 1

    def calcviewed(self):
        d = self.viewed
	if (d.year > 2000):
            return 1
	else:
	    return 0

    isviewed = property(calcviewed)

    def __unicode__(self):
        return self.value
