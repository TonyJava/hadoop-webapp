#coding:utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class message(models.Model):
    #ItemId = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    content = models.TextField()
    filetype = models.IntegerField(default=2)

class fraudphone(models.Model):
	phonenumber = models.CharField(max_length=50)
	phonecontent = models.TextField()
	phonefilename = models.CharField(max_length=100)
	phonetype = models.IntegerField(default=2)   #0 - 诈骗电话 1 - 正常电话 2 - 不确定