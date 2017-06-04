#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import message
from .models import spiderphone
import codecs
import uuid
import time
import fenci
import spider
import test_fraud
# Create your views here.

def index(request):
    return render(request, 'index.html')

def check(request):
	return render(request, 'check.html')

def content(request):
    phone = request.POST['content']
    result = ""
    data = spiderphone.objects.filter(phonenumber = phone).first()
    if data is None:
        result = "noresult"
    else:
        result = data.phonenumber
    return HttpResponse(result)

def checkphone(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        result = "ok"
    else:
        phone = request.GET['phone']
        data = spiderphone.objects.filter(phonenumber = phone).first()
        if data is None:
            result = spider.query_qq('phone', phone)
            if result == 'notknown':
                result = spider.query_360('phone', phone)
                if result != 'notknown':
                    result = "fraud"
        else:
            result = "fraud"    
    return HttpResponse(result)

def checkphonecontent(request):
    if request.method == 'POST':
        phonecontent = request.POST['phonecontent']
        f = codecs.open('D:/trainSet/beiyesi/mytestphone/phone/fraudphone/phone.txt','w','utf-8')
        f.write(phonecontent)
        result = test_fraud.testphoneresult()
        #test_fraud.deletephonefile()
    return HttpResponse(result)

def checksms(request):
    if request.method == 'POST':
        sms = request.POST['sms']
        #result = fenci.fencisms(sms)
        #fname = str(uuid.uuid1())
        f = codecs.open('D:/trainSet/beiyesi/mytestsms/sms/fraudsms/sms.txt','w','utf-8')
        f.write(sms)
        f.close()
        getresult = test_fraud.testsmsresult()
        #test_fraud.deletesmsfile()
    return HttpResponse(getresult)

def testphone(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        type = request.POST['type']
        if type == '1':
            c = "ok"
        else:
            c = "notok"
    else:
        phone = request.GET['phone']
        type = request.GET['type']
        if type == '1':
            data = spiderphone.objects.filter(phonenumber = phone).first()
            if data is None:
                c = "ok"
            else:
                spiderphone.objects.filter(phonenumber = phone).delete()
                c = "notok"
        else:
            spiderphone.objects.create(phonenumber = phone)
            c = "ok"
    return HttpResponse(c)

def testsms(request):
    if request.method == 'POST':
        sms = request.POST['sms']
        type = request.POST['type']
        if type == '1':
            c = "ok"
        else:
            c = "notok"
    else:
        sms = request.GET['sms']
        type = request.GET['type']
        if type == '1':
            c = "ok"
        else:
            c = "notok"
    return HttpResponse(c)

def sparksms(request):
    if request.method == 'POST':
        sms = request.POST['sms']
        result = fenci.fencisms(sms)
        fname = str(uuid.uuid1())
        f = codecs.open('D:/'+fname+'.txt','w','utf-8')
        f.write(fname+","+result)
        f.close()
        #mdata = message.objects.create(filename=fname,content=result)
        #mdata.save()
        for num in range(1,5):
            time.sleep(1)
            try:
                data = message.objects.get(filename = fname)
            except message.DoesNotExist:
                result = "noresult"
            else:
                result = data.filetype
                break
        #result = "ok"
    else:
        sms = request.GET['sms']
        result = "ok"
    return HttpResponse(result)
