'''This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This module defines the primitives for manipulating textual documents. 
'''

from core import Statement, Mention, Generator

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re

class TextualStatement(Statement):

    def __init__(self, text):
        self.text = text
        self.parsed = self.parse(text)

    def getData(self):
        return self.parsed

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


t = TextualStatement('Attorney General Loretta Lynch is declining to comply with an investigation by leading members of Congress about the Obama administration’s secret efforts to send Iran $1.7 billion')
print(t.getAllValidMentions())

