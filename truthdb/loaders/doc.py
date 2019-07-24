'''This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This module defines the primitives for manipulating textual documents. 

CORE_NLP_PATH = '/Users/sanjaykrishnan/Documents/fact-checking/stanford-corenlp-full-2018-10-05'
'''

from .core import Statement, Generator

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

import re
import os
import subprocess

class TextualStatement(Statement):

    def __init__(self, text, src):
        self.text = text
        self.parsed = self.parse(text)

        super(TextualStatement, self).__init__(src)

    def getData(self):
        return self.parsed

    def getRawData(self):
        return self.text

    def getAllValidMentions(self):
        return [p for p in self.parsed if len(p.strip()) > 0]

    def parse(self, text):
        sent = [word for word in nltk.word_tokenize(text)]
        sent = nltk.pos_tag(sent)
        parsed_tokens = self.parseNoun(sent)
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

    def __iter__(self):
        return iter(self.getAllValidMentions())



class DocumentSentenceGenerator(Generator):

    def __init__(self, args):
        f = open(args['filename'], 'r')
        text = ' '.join(f.readlines())
        self.filename = args['filename']
        super(DocumentSentenceGenerator, self).__init__(sent_tokenize(text))

    def prot_load(self):
        rtn = set()
        for d in self.iterator:
            rtn.add(TextualStatement(d, self.filename))
        return rtn