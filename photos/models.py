import os
from django.db import models
from account.models import MyUser

# Create your models here.

class PGalleries(models.Model):
    SERVICE_ID = 27
    spec_id = models.ForeignKey('medtus.Specialities', db_column='spec_id', null=True, blank=True)
    user = models.ForeignKey(MyUser, db_column='user_id', related_name='+')
    title = models.CharField(max_length=255, db_column='title', unique=False)
    description = models.TextField(db_column='description')
    image = models.CharField(max_length=255, blank=True, db_column='image')
    premoder = models.BooleanField(db_column='premoder')
    status = models.BooleanField(db_column='status')
    createdate = models.DateTimeField(auto_now_add=True, db_column='createdate')
    public_main = models.BooleanField(blank=True, default=0)

    class Meta:
        db_table = 'PGalleries'

    def GetPGPhotosList(self):
        return PGPhotos.objects.filter(gallery = self)

    PGPhotosList = property(GetPGPhotosList)

    def treeComments(self, pid=0, level=0, overflow=0, arr=[], start=0, end=None):
        from comments.models import Comments
        from medtus.models import Statistics
        query = Comments.objects.filter(object_id=self.id, service_id=self.SERVICE_ID, parent_id=pid).order_by(
            'createdate')[start:end]
        if pid == 0:
            arr = []
        for comment in query:
            statistics = Statistics.objects.filter(material_id=comment.id, service_id=9999)
            if statistics:
                arr.append([comment, level, 350 - level, statistics[0]])
            else:
                arr.append([comment, level, 350 - level, ''])
            level = level + 20
            if level > 40:
                level = 40
                overflow = overflow + 1
            self.treeComments(comment.id, level, overflow, arr, 0, None)
            overflow = overflow - 1
            if overflow < 0:
                level = level - 20
                overflow = 0
        return arr

    def calcComments(self):
        from comments.models import Comments
        start = Comments.objects.filter(object_id=self.id, service_id=self.SERVICE_ID, parent_id=0).count() - 2
        if start < 0:
            start = 0
        return self.treeComments(0, 0, 0, [], start, None)

    def calcHiddenComments(self):
        from comments.models import Comments
        end = Comments.objects.filter(object_id=self.id, service_id=self.SERVICE_ID, parent_id=0).count() - 2
        if end > 0:
            return self.treeComments(0, 0, 0, [], 0, end)

    comments_list = property(calcComments)
    hidden_comments = property(calcHiddenComments)


class PGPhotos(models.Model):
    gallery = models.ForeignKey(PGalleries, db_column='pgallery_id')
    user = models.ForeignKey(MyUser, db_column='user_id', blank=True, null=True)
    title = models.CharField(max_length=255, db_column='title', unique=False)
    description = models.TextField(db_column='description')
    image = models.FileField(upload_to='pgphotos_images', blank=True, db_column='image')
    status = models.BooleanField(db_column='status')
    createdate = models.DateTimeField(auto_now_add=True, db_column='createdate')
    updatedate = models.DateTimeField(auto_now=True, db_column='updatedate')
    comment_cnt = models.IntegerField(db_column='comment_cnt', default=0)
    rating = models.IntegerField(db_column='rating', default=0)
    votes = models.IntegerField(db_column='votes', default=0)

    class Meta:
        db_table = 'PGPhotos'

    @property
    def filename(self):
        return os.path.basename(self.file.name)
