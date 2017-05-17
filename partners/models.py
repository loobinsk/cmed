from django.db import models

# Create your models here.

class Rubric(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    def __unicode__(self):
        return self.name

class Partner(models.Model):
    image = models.FileField(upload_to='partners_images', blank=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    rubric = models.ForeignKey(Rubric)
    
