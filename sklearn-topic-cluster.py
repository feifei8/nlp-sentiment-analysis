# coding: utf-8
__author__ = 'zhourunlai'

import pandas as pd
import re
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralCoclustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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

    # 分句
    comma_tokenizer = lambda x: re.split(r'\s+|[,;.-]\s*', x)
    vectorizer = TfidfVectorizer(tokenizer=comma_tokenizer)
    train_data = vectorizer.fit_transform(train_words)
    test_data = vectorizer.transform(test_words)

    # 聚类
    # clf = KMeans(n_clusters=20)
    # clf = DBSCAN(eps=0.5, min_samples=5, random_state=None)
    clf = SpectralCoclustering(n_clusters=20, svd_method='arpack', random_state=0)
    clf.fit(train_data)

    # 中心点
    # print(clf.cluster_centers_)

    # 每个样本所属的簇
    # print(clf.labels_)
    # i = 1
    # while i <= len(clf.labels_):
    #     print i, clf.labels_[i - 1]
    #     i += 1

    # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    # print(clf.inertia_)

    # i = 1
    # while i <= len(clf.row_labels_):
    #     print i, words[i], clf.row_labels_[i - 1]
    #     i += 1

    pca = PCA(n_components=3)  # 输出两维
    newData = pca.fit_transform(train_data.toarray())  # 载入N维
    print newData

    x1 = []
    y1 = []
    i = 0
    while i < 240:
        x1.append(newData[i][0])
        y1.append(newData[i][1])
        i += 1

    x2 = []
    y2 = []
    i = 240
    while i < 480:
        x2.append(newData[i][0])
        y2.append(newData[i][1])
        i += 1

    x3 = []
    y3 = []
    i = 480
    while i < 720:
        x3.append(newData[i][0])
        y3.append(newData[i][1])
        i += 1

    plt.plot(x1, y1, 'or')
    plt.plot(x2, y2, 'og')
    plt.plot(x3, y3, 'ob')
    plt.show()