# coding: utf-8
__author__ = 'zhourunlai'

import pandas as pd
import re
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cluster import KMeans

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
    comma_tokenizer = lambda x: re.split(r'\s+|[,;.-]\s*', x)
    vectorizer = HashingVectorizer(tokenizer=comma_tokenizer)
    train_data = vectorizer.fit_transform(train_words)
    test_data = vectorizer.transform(test_words)

    # 聚类
    clf = KMeans(n_clusters=4)
    clf.fit(train_data)
    print clf.cluster_centers_
