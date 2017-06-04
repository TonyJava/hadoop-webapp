# -*- coding: UTF-8 -*-
import sys
import os
import shutil
import jieba
import cPickle as pickle#导入cPickle包并且取一个别名pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB  # 导入多项式贝叶斯算法
# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

# 保存至文件
def savefile(savepath, content):
    with open(savepath, "wb") as fp:
        fp.write(content)
# 读取文件
def readfile(path):
    with open(path, "rb") as fp:
        content = fp.read()
    return content

def corpus_segment(corpus_path, seg_path):
    '''
    corpus_path是未分词语料库路径
    seg_path是分词后语料库存储路径
    '''
    catelist = os.listdir(corpus_path)  # 获取corpus_path下的所有子目录
    '''
    其中子目录的名字就是类别名，例如：
    train_corpus/art/21.txt中，'train_corpus/'是corpus_path，'art'是catelist中的一个成员
    '''

    # 获取每个目录（类别）下所有的文件
    for mydir in catelist:
        '''
        这里mydir就是train_corpus/art/21.txt中的art（即catelist中的一个类别）
        '''
        class_path = corpus_path + mydir + "/"  # 拼出分类子目录的路径如：train_corpus/art/
        seg_dir = seg_path + mydir + "/"  # 拼出分词后存贮的对应目录路径如：train_corpus_seg/art/

        if not os.path.exists(seg_dir):  # 是否存在分词目录，如果没有则创建该目录
            os.makedirs(seg_dir)

        file_list = os.listdir(class_path)  # 获取未分词语料库中某一类别中的所有文本
        '''
        train_corpus/art/中的
        21.txt,
        22.txt,
        23.txt
        ...
        file_list=['21.txt','22.txt',...]
        '''
        for file_path in file_list:  # 遍历类别目录下的所有文件
            fullname = class_path + file_path  # 拼出文件名全路径如：train_corpus/art/21.txt
            content = readfile(fullname)  # 读取文件内容
            '''此时，content里面存贮的是原文本的所有字符，例如多余的空格、空行、回车等等，
            接下来，我们需要把这些无关痛痒的字符统统去掉，变成只有标点符号做间隔的紧凑的文本内容
            '''
            content = content.replace("\r\n", "")  # 删除换行
            content = content.replace(" ", "")#删除空行、多余的空格
            content_seg = jieba.cut(content)  # 为文件内容分词
            savefile(seg_dir + file_path, " ".join(content_seg))  # 将处理后的文件保存到分词后语料目录
    #print "中文语料分词结束！！！"
    return "ok"

def corpus2Bunch(wordbag_path,seg_path):
    catelist = os.listdir(seg_path)# 获取seg_path下的所有子目录，也就是分类信息
    #创建一个Bunch实例
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(catelist)
    '''
    extend(addlist)是python list中的函数，意思是用新的list（addlist）去扩充
    原来的list
    '''
    # 获取每个目录下所有的文件
    for mydir in catelist:
        class_path = seg_path + mydir + "/"  # 拼出分类子目录的路径
        file_list = os.listdir(class_path)  # 获取class_path下的所有文件
        for file_path in file_list:  # 遍历类别目录下文件
            fullname = class_path + file_path  # 拼出文件名全路径
            bunch.label.append(mydir)
            bunch.filenames.append(fullname)
            bunch.contents.append(readfile(fullname))  # 读取文件内容
            '''append(element)是python list中的函数，意思是向原来的list中添加element，注意与extend()函数的区别'''
    # 将bunch存储到wordbag_path路径中
    with open(wordbag_path, "wb") as file_obj:
        pickle.dump(bunch, file_obj)
    #print "构建文本对象结束！！！"
    return "ok"

def readbunchobj(path):
    with open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch

def writebunchobj(path, bunchobj):
    with open(path, "wb") as file_obj:
        pickle.dump(bunchobj, file_obj)

def vector_space(stopword_path,bunch_path,space_path,train_tfidf_path=None):

    stpwrdlst = readfile(stopword_path).splitlines()
    bunch = readbunchobj(bunch_path)
    tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[], vocabulary={})

    if train_tfidf_path is not None:
        trainbunch = readbunchobj(train_tfidf_path)
        tfidfspace.vocabulary = trainbunch.vocabulary
        vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5,vocabulary=trainbunch.vocabulary)
        tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)

    else:
        vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5)
        tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
        tfidfspace.vocabulary = vectorizer.vocabulary_

    writebunchobj(space_path, tfidfspace)
    #print "if-idf词向量空间实例创建成功！！！"
    return "ok"

def testphoneresult():
    corpus_path = "D:/trainSet/beiyesi/mytestphone/phone/"  # 未分词分类语料库路径
    seg_path = "D:/trainSet/beiyesi/mytestphone/phone_seg/"  # 分词后分类语料库路径
    corpus_segment(corpus_path, seg_path)
    wordbag_path = "D:/trainSet/beiyesi/mytestphone/test_set.dat"  # Bunch存储路径
    corpus2Bunch(wordbag_path, seg_path)
    space_path = "D:/trainSet/beiyesi/mytestphone/testspace.dat"
    train_tfidf_path = "D:/trainSet/beiyesi/mytrainphone/tfdifspace.dat"
    stopword_path = "D:/pythonWorkspace/chinese_text_classification-master/train_word_bag/hlt_stop_words.txt"
    vector_space(stopword_path, wordbag_path, space_path, train_tfidf_path)
    # 导入训练集
    #trainpath = "D:/pythonWorkspace/chinese_text_classification-master/sms_bag/tfdifspace.dat"
    #train_set = readbunchobj(trainpath)

    # 导入测试集
    #testpath = "D:/pythonWorkspace/chinese_text_classification-master/sms_bag/testspace.dat"
    test_set = readbunchobj(space_path)
    # 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高
    #clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)
    # joblib.dump(clf, "D:/pythonWorkspace/chinese_text_classification-master/sms_bag/train_model.m")
    clf = joblib.load("D:/trainSet/beiyesi/mytrainphone/train_model.pkl")
    # 预测分类结果
    predicted = clf.predict(test_set.tdm)

    for flabel, file_name, expct_cate in zip(test_set.label, test_set.filenames, predicted):
        print file_name, ": 实际类别:", flabel, " -->预测类别:", expct_cate
        if flabel != expct_cate:
            return "预测为正常电话"
        else:
            return "预测为诈骗电话"

def testsmsresult():
    corpus_path = "D:/trainSet/beiyesi/mytestsms/sms/"  # 未分词分类语料库路径
    seg_path = "D:/trainSet/beiyesi/mytestsms/sms_seg/"  # 分词后分类语料库路径
    corpus_segment(corpus_path, seg_path)
    wordbag_path = "D:/trainSet/beiyesi/mytestsms/test_set.dat"  # Bunch存储路径
    corpus2Bunch(wordbag_path, seg_path)
    space_path = "D:/trainSet/beiyesi/mytestsms/testspace.dat"
    train_tfidf_path = "D:/trainSet/beiyesi/mytrainsms/tfdifspace.dat"
    stopword_path = "D:/pythonWorkspace/chinese_text_classification-master/train_word_bag/hlt_stop_words.txt"
    vector_space(stopword_path, wordbag_path, space_path, train_tfidf_path)

    #space_path = "D:/pythonWorkspace/chinese_text_classification-master/test_bag/sms_seg/testspace.dat"
    # 导入训练集
    #trainpath = "D:/pythonWorkspace/chinese_text_classification-master/sms_bag/tfdifspace.dat"
    #train_set = readbunchobj(trainpath)

    # 导入测试集
    #testpath = "D:/pythonWorkspace/chinese_text_classification-master/sms_bag/testspace.dat"
    test_set = readbunchobj(space_path)
    # 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高
    #clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)
    # joblib.dump(clf, "D:/pythonWorkspace/chinese_text_classification-master/sms_bag/train_model.m")
    clf = joblib.load("D:/trainSet/beiyesi/mytrainsms/train_model.pkl")
    # 预测分类结果
    predicted = clf.predict(test_set.tdm)

    for flabel, file_name, expct_cate in zip(test_set.label, test_set.filenames, predicted):
        #print file_name, ": 实际类别:", flabel, " -->预测类别:", expct_cate
        if flabel != expct_cate:
            return "normal"
        else:
            return "fraud"


def deletesmsfile():
    """
    fucking 
    """
    shutil.rmtree("D:/trainSet/beiyesi/mytestphone/phone_seg/")
    shutil.rmtree("D:/trainSet/beiyesi/mytestphone/test_set.dat")
    shutil.rmtree("D:/trainSet/beiyesi/mytestphone/testspace.dat")


def deletephonefile():
    """
    fucking
    """
    shutil.rmtree("D:/trainSet/beiyesi/mytestphone/phone_seg/")
    os.remove("D:/trainSet/beiyesi/mytestphone/test_set.dat")
    os.remove("D:/trainSet/beiyesi/mytestphone/testspace.dat")


#print testsmsresult()

