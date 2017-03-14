#!/usr/bin/python2.7
# _*_ coding: utf-8 _*_

"""
@Author: xiaolingu
"""
import math
import numpy as np
import os
import copy


class Tokentext():
    def __init__(self, text = '', token = 0):
        self.text = text 
        self.token = token
    def setTokentext(self, text, token):
        self.text = text
        self.token = token 
    def setText(self, text):
        self.text = text
    def getText(self):
        return self.text
    def getToken(self):
        return self.token
    def setToken(self, token):
        self.token = token

class AllData():
    def textParser(self, text):
        import re
        regEx = re.compile(r'[^a-zA-Z]|\d')  # 匹配非字母或者数字，即去掉非字母非数字，只留下单词
        words = regEx.split(text)
        # 去除空字符串，并统一小写
        words = [word.lower() for word in words if len(word) > 0]
        return words

    def Token(self, DocumentData) :
        if DocumentData == 'ham':
            classCategory = 0
        elif DocumentData == 'spam':
            classCategory = 1
        return classCategory

    def texttoken(self):
        fp = open(r'C:\Users\xiaolin\Desktop\naivebayes\emails\training\SMSCollection.txt', 'r')
        Line = 0
        content = fp.readlines()
        AllLines = len(content)
        TokentextInstance = [Tokentext() for i in range(AllLines)]
        for line in content:
            linedata = line.strip().split('\t')
            token = self.Token(linedata[0])
            text = linedata[1]
            text_no_number = self.textParser(text)
            if(self.LongStringNumber(text)):
                text = text_no_number + ['longStringNumber']
            else:
                text = text_no_number
            TokentextInstance[Line].setTokentext(text, token)
            Line = Line + 1
        return TokentextInstance
    def LongStringNumber(self, text):
        import re
        regEx = re.compile(r'\d{3,}')  
        LongStringNumber = regEx.findall(text)
        if (LongStringNumber == []):
            return False
        else:
            return True

class CountSpamHam():
    def __init__(self, SpamSum = 0, HamSum = 0):
        self.SpamSum = SpamSum
        self.HamSum = HamSum

    def set(self, TokentextInstance):
        for Tokentext in TokentextInstance:
            if Tokentext.getToken() == 0 :
                self.HamSum = self.HamSum + 1
            elif Tokentext.getToken() == 1 :
                self.SpamSum = self.SpamSum + 1
    def getSpamSum(self):
        return self.SpamSum

    def getHamSum(self):
        return self.HamSum

class vector():
    def __init__(self, vocabulary = None, SpamNumber = 0, HamNumber = 0):
        self.vocabulary = vocabulary
        self.SpamNumber = SpamNumber
        self.HamNumber = HamNumber

    def getvocabulary(self):
        return self.vocabulary

    def getSpamNumber(self):
        return self.SpamNumber
    
    def getHamNumber(self):
        return self.HamNumber
    
    def setHamNumber(self, HamNumber):
        self.HamNumber = HamNumber

    def setSpamNumber(self, SpamNumber):
        self.SpamNumber = SpamNumber

    def setvocabulary(self, vocabulary):
        self.vocabulary = vocabulary
    def addSpamNumber(self):
        self.SpamNumber = self.SpamNumber + 1
    def addHamNumber(self):
        self.HamNumber = self.HamNumber + 1

class vectorProbability():
    def __init__(self, vocabulary = None, SpamP = 0.000035, HamP = 0.000035):
        self.vocabulary = vocabulary
        self.SpamP = SpamP
        self.HamP = HamP

    def getvocabulary(self):
        return self.vocabulary

    def getSpamP(self):
        return self.SpamP
    
    def getHamP(self):
        return self.HamP
    
    def setHamP(self, HamP):
        self.HamP = HamP

    def setSpamP(self, SpamP):
        self.SpamP = SpamP

    def setvocabulary(self, vocabulary):
        self.vocabulary = vocabulary
    def getvocabulary(self):
        return self.vocabulary

def creatWordList(TokentextInstance):
    Words = []
    for text in TokentextInstance:
        Words =  Words + text.getText()
    return Words 

def FormFeature(Words):
    vocabularySet = set(Words)
    vocabularyList = list(vocabularySet)
    return vocabularyList

def CheckEqual(a, b):
    if a == b:
        return True
    else:
        return False

class Probablity(object):
    def Logdivide(self, a, b):
        return np.log(float(a)/float(b))

class Table():
    def crateTable(self, VocabularyList, TokentextInstance):
        Tablespamham = [vector() for i in range(len(VocabularyList))]
        for (index, Vocabulary) in enumerate(VocabularyList) :
            CurrentVector = Tablespamham[index - 1]
            CurrentVector.setvocabulary(Vocabulary)
            for Tokentext in TokentextInstance:
                Words = Tokentext.getText()
                Token = Tokentext.getToken()
                if Vocabulary in Words :
                    if (CheckEqual(Token , 0)):
                        CurrentVector.addHamNumber()
                    elif (CheckEqual(Token, 1)):
                        CurrentVector.addSpamNumber()
        return Tablespamham
    def createEmptyTable(self, VocabularyList):
        EmptyTable = [vectorProbability() for i in range(len(VocabularyList))]
        return EmptyTable

    def createProbablity(self, VocabularyList, TokentextInstance):
        countspamham = CountSpamHam()
        countspamham.set(TokentextInstance)
        SpamSum = countspamham.getSpamSum()
        HamSum = countspamham.getHamSum()
        EmptyTable = self.createEmptyTable(VocabularyList)
        Tablespamham = self.crateTable(VocabularyList, TokentextInstance)
        for (index, word) in enumerate(VocabularyList):
            EmptyTable[index - 1].setvocabulary(word)
            EmptyTable[index - 1].setSpamP(Probablity().Logdivide(Tablespamham[index - 1].getSpamNumber(),SpamSum))
            EmptyTable[index - 1].setHamP(Probablity().Logdivide(Tablespamham[index - 1].getHamNumber(), HamSum)) 
        return EmptyTable
    def OutfileofTable(self,EmptyTable):
        fp = open(r'.\ProbabilityTable.txt','w')
        for x in xrange(0,len(EmptyTable)):
            aline = EmptyTable[x].getvocabulary(),str(EmptyTable[x].getSpamP()),str(EmptyTable[x].getHamP()) + '\n' 
            fp.writelines(aline)
        fp.close()
    def outnumber(self,Tablespamham):
        fp = open(r'.\NumberTable.txt','w')
        aline = "word\tSpam\tHam\n"
        fp.writelines(aline)
        for x in xrange(0,len(Tablespamham)):
            aline = Tablespamham[x].getvocabulary() + '\t' + str(Tablespamham[x].getSpamNumber())+ '\t' + str(Tablespamham[x].getHamNumber()) + '\n' 
            fp.writelines(aline)
        fp.close()



def Predict(index, Tokentexts, ProbablityTable):
    Words = Tokentexts[index].getText()
    vocabulary = FormFeature(Words)
    LogSpamPSum = 0
    LogHamPSum = 0
    for word in vocabulary:
        for (i, Tablevector) in enumerate(ProbablityTable):
            if (word == Tablevector.getvocabulary()):
                LogSpamPSum = Tablevector.getSpamP() + LogSpamPSum
                LogHamPSum = Tablevector.getHamP() + LogHamPSum


    a = copy.deepcopy(CountSpamHam())
    a.set(Tokentexts)        
    HamSum = a.getHamSum()
    SpamSum = a.getSpamSum()

    LogSpamAll = Probablity().Logdivide(SpamSum, HamSum + SpamSum)
    LogHamAll = Probablity().Logdivide(HamSum, HamSum + SpamSum)

    LogSpamPSum = LogSpamAll + LogSpamPSum
    LogHamPSum = LogHamAll + LogHamPSum
    if((LogHamPSum >= LogSpamPSum)&(Tokentexts[index - 1].getToken() == 0)):
        return True
    elif(LogHamPSum <= LogSpamPSum)&(Tokentexts[index - 1].getToken() == 1):
        return True
    else :
        return False




