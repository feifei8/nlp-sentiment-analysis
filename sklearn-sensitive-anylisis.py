# encoding=utf-8

# 导入数据
import numpy as np

path = u'spide/output/疯狂动物城 Zootopia.txt'
data = np.loadtxt(path, delimiter='\t', dtype=np.str)

# 打乱
from random import shuffle

shuffle(data)

# 生成训练集和测试集
development = data[:900, :]
test = data[900:, :]
train = development[:, 1:]
tag = development[:, 0].astype(np.float)

# 分类
import sklearn
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

svc = svm.SVC(gamma=0.001, C=100.)

lr = LogisticRegression(penalty='l1', tol=0.01)

gnb = GaussianNB()

# 交叉验证
from sklearn import cross_validation

kfold = cross_validation.KFold(len(development), n_folds=10)

# 精确度
svc_accuracy = cross_validation.cross_val_score(svc, train, tag, cv=kfold)

lr_accuracy = cross_validation.cross_val_score(lr, train, tag, cv=kfold)

gnb_accuracy = cross_validation.cross_val_score(gnb, train, tag, cv=kfold)

print 'SVM average accuary: %f' % svc_accuracy.mean()

print 'LogisticRegression average accuary: %f' % lr_accuracy.mean()

print 'Naive Bayes average accuary: %f' % gnb_accuracy.mean()
