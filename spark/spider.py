# coding: utf-8

import re
import json
import time

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

#labels = query_360('phone', '13102416011')
#if labels == 'notknown':
#    print '未知状态电话号码-360'
#else:
#    for label in labels:
#        print u'被{0:3d}用户标记为 {1}, 数据来源 {2}'.format(label[u'labelNum'], label[u'label'], label[u'labelSrc'])


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


#r2 = query_qq('phone', '18362916020')
#if r2 == 'notknown':
#    print '未知状态的号码-qq'
#else:
#    print r2



