# -*- coding: utf-8 -*-

"""
演示使用NLTK让计算机学习如何通过名字识别性别。
"""

import nltk

# 定义学习方法
def gender_features(word):
    return {'last_letter':word[-1]}

# 导入学习的姓名性别名单
from nltk.corpus import names
import random
names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)

# 开始学习
featuresets = [(gender_features(n), g) for (n, g) in names]
trainset, testset = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(trainset)

# 使用分类器进行分类
print classifier.classify(gender_features('Neo'))
print classifier.classify(gender_features('Trinity'))

# 用测试集来测试
print nltk.classify.accuracy(classifier, testset)

# 显示出区分度最高的几个features
print classifier.show_most_informative_features(5)