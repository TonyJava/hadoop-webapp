# coding: utf-8

import re
import json
import time
from .models import spiderphone
import requests

def query_360(qtype, q):
    payload = {
        'timeout': '5000',
        'type':  qtype,
        'q': q,
    }
    headers = {
        'Referer': 'https://110.360.cn/',
    }

    search_url = 'https://110.360.cn/interface/search'
    r = requests.get(search_url, params=payload, headers=headers)
    res = json.loads(r.content)
    if res.get('errno') != 0:
        #print res.get('errmsg', ' no err msg')
        return "notknown"
    data = res.get('data')

    datastr = str(data.get('labels'))
    if datastr == "[]":
        return 'notknown'
    else:
        return data.get('labels', [])[1]

def query_qq(qtype, q):
    data = {
        'm': 'check',
        'a': 'run',
        'callback': 'fuckjsonp',
        'keys': q,
        'action': qtype,
        'time': int(time.time()*1000)
    }
    url = 'http://txwz.qq.com/lib/index.php'
    r = requests.get(url, params=data)
    result = json.loads(r.content[10:-1])
    if result.has_key('uTagC'):
        return result[u'uTagC']
    else:
        return "notknown"

def phonetosql():
    fphone = open("D:\\trainSet\\allspiderfraudphone.txt")
    try:
        phones = fphone.read()
        phones = unicode(phones, 'utf8')
    finally:
        fphone.close()
    for myword in phones.split("\n"):
        phone = spiderphone.objects.create(phonenumber=myword)
        phone.save()
