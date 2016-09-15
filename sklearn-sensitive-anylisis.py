# encoding=utf-8
__author__ = 'zhourunlai'

# 导入数据
import pandas as pd
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

path = u'spide/output/疯狂动物城 Zootopia.txt'
data = pd.read_csv(path, sep='\t', header=None)

text = data[1]
tag = data[0]

text_new = []
for i in text:
    seg_list = jieba.cut(i.strip())
    text_new.append(' '.join(seg_list))
# print text_new

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

tf = vectorizer.fit_transform(text_new)
tfidf = transformer.fit_transform(tf)
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
# for i in range(len(weight)):
#     for j in range(len(word)):
#         print word[j], weight[i][j]
print weight
