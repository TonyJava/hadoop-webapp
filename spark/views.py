#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import message
import codecs
import uuid
import time
# Create your views here.
def index(request):
    return render(request, 'index.html')

def check(request):
	return render(request, 'check.html')

def content(request):
    fname = str(uuid.uuid1())
    f = codecs.open('D:/'+fname+'.txt','w','utf-8')
    content = request.POST['content']
    f.write(fname+","+content)
    #mdata = message.objects.create(filename=fname,content=content)
    #mdata.save()
    for num in range(1,10):
    	time.sleep(1)
        try:
	        data = message.objects.get(filename = fname)
        except message.DoesNotExist:
            result = "Apress isn't in the database yet."
        else:
            result = data.filetype
            break
    return HttpResponse(result)
    #name = "8ef636de-0ecb-11e7-b166-6002b4bf1daf"
	#mdata = message.objects.create(filename=fname,content=content)
	#mdata.save()