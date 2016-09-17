# coding: utf-8
__author__ = 'zhourunlai'

import pandas as pd
import jieba
import numpy
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.svm import LinearSVC

if __name__ == "__main__":
    # 加载数据
    path = u'spide/output/疯狂动物城 Zootopia.txt'
    dataset = pd.read_csv(path, sep='\t', header=None)
    print "样本数目：%d" % len(dataset)

    # 数据预处理
    tags = dataset[0]
    words = dataset[1]

    # 生成训练集和测试集
    train_tags, test_tags = train_test_split(tags, test_size=0.3)
    train_words, test_words = train_test_split(words, test_size=0.3)
    print "训练集数目：%d; 测试集数目：%d" % (len(train_words), len(test_words))

    # 分词
    comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)
    vectorizer = TfidfVectorizer(tokenizer=comma_tokenizer)
    train_data = vectorizer.fit_transform(train_words)
    test_data = vectorizer.transform(test_words)

    # 分类
    # clf = LogisticRegression()
    clf = MultinomialNB(alpha=0.01)
    # clf = svm.SVC()
    # clf = LinearSVC()
    clf.fit(train_data, numpy.asarray(train_tags))

    # 验证
    actual = numpy.asarray(test_tags)
    pred = clf.predict(test_data)
    m_precision = metrics.precision_score(actual, pred)
    m_recall = metrics.recall_score(actual, pred)
    print '预测准确率:{0:.3f}'.format(m_precision)
    print '预测召回率:{0:0.3f}'.format(m_recall)
