from __future__ import unicode_literals

from django.db import models

# Create your models here.
class message(models.Model):
    #ItemId = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    content = models.TextField()
    filetype = models.IntegerField(default=2)