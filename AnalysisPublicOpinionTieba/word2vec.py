# coding=utf-8
import numpy
from gensim.models import word2vec
import  gensim
import os
import numpy as np
import os.path
import sys
# import jieba
import codecs
import logging
# reload(sys)
# sys.setdefaultencoding('utf-8')


#分词处理
def wordSort():
    contents = codecs.open(r'E:\test.txt','r',encoding='utf-8')
    result_contents = codecs.open(r'E:\result_test1.txt','w',encoding='utf-8')
    #把分词的结果放到result_test.txt中
    for content in contents:
        print(content.decode("utf-8"))
        sortWord = jieba.cut(content,cut_all=False)
        result_contents.write(" ".join(sortWord))

    contents.close()
    result_contents.close()


#语料的训练
def wordPro():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(u"C:\\Users\\xujiajun\\Desktop\\word2vec\\corpus.txt")
    # 第一个参数是训练语料，第二个参数是小于该数的单词会被剔除，默认值为5,我一开始的时候用的是5，又因为我训练的样本太少导致数不出结果
    # 改成1之后就好了
    # 第三个参数是神经网络的隐藏层单元数，默认为100
    model = word2vec.Word2Vec(sentences,size =200,min_count=5,sg=0,alpha=0.025)
    # y1 = model.similarity(u"互联网", u"计算机")
    # print u"【互联网】和【计算机】的相似度为：", y1
    # print "--------\n"

    # 若训练的语料中没有中国就会报错，因为我上面训练的时候量至少为1
    y2 = model.most_similar(u"主席", topn=20)  # 20个最相关的
    #print u"和【中国】最相关的词有：\n"
    for item in y2:
        print(item[0], item[1])
    print("--------\n")
    # 训练的时间较长,将训练好的模型保存下来
    model.save(u"WordVec.model")



# 模型的调用
def useModleTest():
    model = gensim.models.Word2Vec.load(u"WordVec.model")
    # y1 = model.most_similar(u"王后", topn=20)  # 20个最相关的
    # print model[u'记者']
    # for item in y1:
    #     print item[0], item[1]
    # print "--------\n"

    y2 = model.most_similar(positive=[u'男人', u'女人'], negative=[u'国王'],topn=1)
    for item in y2:
        print(item[0], item[1])
    print("--------\n")

if __name__ == '__main__':
    wordPro()
    # useModleTest()
