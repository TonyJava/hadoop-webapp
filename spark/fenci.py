#-*- coding:utf-8 -*-
import jieba


def fencisms(sms):
    seg_list = jieba.cut(sms, cut_all=False)
    liststr = "/".join(seg_list)
    f_stop = open('D:\pythonWorkspace\DjangoWorkspace\hadoop\spark\stop.txt')
    try:
        f_stop_text = f_stop.read()
        f_stop_text = unicode(f_stop_text, 'utf8')
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split("\n")
    word = ""
    for myword in liststr.split("/"):
        if not (myword.strip() in f_stop_seg_list):
            word += myword
            word += " "
    return word