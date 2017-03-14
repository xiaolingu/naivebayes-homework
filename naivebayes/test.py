#!/usr/bin/python2.7
# _*_ coding: utf-8 _*_
"""
@author:guxiaolin
"""

import Naivebayse as nb
import copy
import random


Tokentexts_All = nb.AllData().texttoken()
Words = nb.creatWordList(Tokentexts_All)
VocabularyList = nb.FormFeature(Words)

'''
交叉验证
'''
count = 0 
MaxofCorrectCount = 0
MinofCorrectCount = 10000
#生成n个不同的随机数
# while(count < 10):
testindex_List = random.sample(range(len(Tokentexts_All)), 500)
trainindex_List = list(set(range(len(Tokentexts_All))) - set(testindex_List))
CorrectCounts = 0;
TrainTokentext = []
TestTokentext = []
Tablespamham = nb.Table().crateTable(VocabularyList, Tokentexts_All)
nb.Table().outnumber(Tablespamham)

#选择训练样本
for i in trainindex_List:
	TrainTokentext.append(Tokentexts_All[i])
ProbablityTable = nb.Table().createProbablity(VocabularyList, TrainTokentext)

for i in testindex_List:
	if(nb.Predict(i, Tokentexts_All, ProbablityTable)):
		CorrectCounts = CorrectCounts + 1

if(CorrectCounts > MaxofCorrectCount):
	MaxofCorrectCount = CorrectCounts
if(CorrectCounts < MinofCorrectCount):
	MinofCorrectCount = CorrectCounts
count = count + 1
print "MaxofCorrectCount:",MaxofCorrectCount,"MinofCorrectCount:",MinofCorrectCount




