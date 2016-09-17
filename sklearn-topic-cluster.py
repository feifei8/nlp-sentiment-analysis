# coding: utf-8

import pandas as pd
import re
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import HashingVectorizer

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
