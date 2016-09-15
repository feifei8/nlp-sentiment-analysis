# encoding=utf-8

import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

path = u'spide/output/疯狂动物城 Zootopia.txt'
originData = pd.read_csv(path, sep='\t', header=None)

rateDocument = originData[1]

fiveRateDocument = rateDocument[originData[0] == 5]
fourRateDocument = rateDocument[originData[0] == 4]
threeRateDocument = rateDocument[originData[0] == 3]
twoRateDocument = rateDocument[originData[0] == 2]
oneRateDocument = rateDocument[originData[0] == 1]

posRateDocument = fiveRateDocument.append(fourRateDocument)
negRateDocument = oneRateDocument.append(twoRateDocument)
allRateDocument = posRateDocument.append(negRateDocument)

corpus = []
for pos in allRateDocument:
    seg = jieba.cut(pos)
    corpus.append(' '.join(seg))

# 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()
# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()

# 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
tf = vectorizer.fit_transform(corpus)
tfidf = transformer.fit_transform(tf)

# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
# 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

# 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
for i in range(len(weight)):
    print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    for j in range(len(word)):
        print word[j], weight[i][j]
