'''This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This module defines the primitives for manipulating textual documents. 
'''

from core import Statement, Mention, Generator,SentimentAnalyzer

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

import re
import os
import subprocess

class TextualStatement(Statement):

    def __init__(self, text):
        self.text = text
        self.parsed = self.parse(text)

    def getData(self):
        return self.parsed

    def getRawData(self):
        return self.text

    def getAllValidMentions(self):
        return set([ContainsMention(p) for p in self.parsed])

    def parse(self, text):
        sent = [word for word in nltk.word_tokenize(text)]
        sent = nltk.pos_tag(sent)
        parsed_tokens = self.parseQuantity(self.parseNoun(sent))
        noun_phrases = [ ' '.join([word[0] for word in p.leaves()])\
                         for p in parsed_tokens \
                         if isinstance(p, nltk.tree.Tree) and p.label() == 'NNG']

        noun_phrases = [re.sub(r'[^\w\s]','',n).strip().lower()\
                         for n in noun_phrases]

        return noun_phrases

    def parseNoun(self, pos):
        pattern = 'NNG: {<NN|NNS|NNP>*}'
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(pos)
        return cs

    def parseQuantity(self, pos):
        pattern = 'CDG: {<CD>*}'
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(pos)
        return cs


class ContainsMention(Mention):

    def __init__(self, obj):
        self.data = obj

    def test(self, data):
        return (obj in data)

    def __str__(self):
        return str({'Mentions': self.data})

    __repr__ = __str__


class StanfordNLPModel(SentimentAnalyzer):

    def __init__(self, data, args):
        super(StanfordNLPModel, self).__init__(data,args)

    def batchAnalyze(self):
        my_env = os.environ.copy()
        my_env["CLASSPATH"] = self.args['install_path'] + "/*"
        process=subprocess.Popen(['java','-mx5g', 'edu.stanford.nlp.sentiment.SentimentPipeline', '-stdin'],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     env=my_env)
        datalst = list([t.getRawData() for t in self.data])
        data = bytes('\n'.join(datalst),'utf-8')
        stdoutdata,stderrdata=process.communicate(input=data)
        predictionlst = str(stdoutdata).split('\\n')
        numerical_predictions = []
        for p in predictionlst:
            if 'Pos' in p:
                numerical_predictions.append(1)
            elif 'Neg' in p:
                numerical_predictions.append(-1)
            else:
                numerical_predictions.append(0)

        return list(zip(list(self.data), numerical_predictions))


class DocumentSentenceGenerator(Generator):

    def __init__(self, filename):
        f = open(filename, 'r')
        text = ' '.join(f.readlines())
        super(DocumentSentenceGenerator, self).__init__(sent_tokenize(text))

    def prot_load(self):
        rtn = set()
        for d in self.iterator:
            rtn.add(TextualStatement(d))
        return rtn


d = DocumentSentenceGenerator('demo.txt')
print(d.load())
s = StanfordNLPModel(d.data, {'install_path': '/Users/sanjayk/Dropbox/fact-checking/contradiction-dep/utils/stanford-corenlp-full-2018-10-05'})
print(s.batchAnalyze())