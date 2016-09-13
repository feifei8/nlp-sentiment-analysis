# encoding=utf-8

import jieba
from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel

try:
    sc.stop()
except:
    pass

APP_NAME = "My Spark Application"


def main(sc):
    pass


if __name__ == "__main__":
    # Spark配置
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 导入文件
    originData = sc.textFile('hdfs:///tmp/output.txt')

    # 数据预处理
    originDistinctData = originData.distinct()
    rateDocument = originDistinctData.map(lambda line: line.split('\t')).filter(lambda line: len(line) == 2)

    # 统计打分情况
    fiveRateDocument = rateDocument.filter(lambda line: int(line[0]) == 5)
    fiveRateDocument.count()
    fourRateDocument = rateDocument.filter(lambda line: int(line[0]) == 5)
    fourRateDocument.count()
    threeRateDocument = rateDocument.filter(lambda line: int(line[0]) == 5)
    threeRateDocument.count()
    twoRateDocument = rateDocument.filter(lambda line: int(line[0]) == 5)
    twoRateDocument.count()
    oneRateDocument = rateDocument.filter(lambda line: int(line[0]) == 5)
    oneRateDocument.count()

    # 生成训练数据
    negRateDocument = oneRateDocument.union(twoRateDocument).union(threeRateDocument)
    negRateDocument.repartition(1)
    posRateDocument = sc.parallelize(fiveRateDocument.take(negRateDocument.count())).repartition(1)
    allRateDocument = negRateDocument.union(posRateDocument)
    allRateDocument.repartition(1)
    # rate = allRateDocument.map(lambda s: ReduceRate(s[0]))
    document = allRateDocument.map(lambda s: s[1])

    # 分词
    words = document.map(lambda w: "/".join(jieba.cut_for_search(w))).map(lambda line: line.split("/"))

    # 训练词频矩阵
    hashingTF = HashingTF()
    tf = hashingTF.transform(words)
    tf.cache()

    # 计算 TF-IDF 矩阵
    idfModel = IDF().fit(tf)
    tfidf = idfModel.transform(tf)

    # 生成训练集和测试集
    zipped = rate.zip(tfidf)
    data = zipped.map(lambda line: LabeledPoint(line[0], line[1]))
    training, test = data.randomSplit([0.6, 0.4], seed=0)

    # 训练贝叶斯分类模型
    NBmodel = NaiveBayes.train(training, 1.0)
    predictionAndLabel = test.map(lambda p: (NBmodel.predict(p.features), p.label))
    accuracy = 1.0 * predictionAndLabel.filter(lambda x: 1.0 if x[0] == x[1] else 0.0).count() / test.count()

    print accuracy

    main(sc)
