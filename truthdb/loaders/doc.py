'''This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This module defines the primitives for manipulating textual documents. 

CORE_NLP_PATH = '/Users/sanjaykrishnan/Documents/fact-checking/stanford-corenlp-full-2018-10-05'
'''

from .core import Loader
from truthdb.exec.rel import DARelation

import nltk
from nltk.tokenize import sent_tokenize, TweetTokenizer
import re



class SentenceLoader(Loader):

    def __init__(self, args):
        super(SentenceLoader, self).__init__(args)

        f = open(self.params['filename'], 'r')
        self.text = ' '.join(f.readlines())
        self.text = self.text.replace(u'\u2019', "'").replace(u'\u201d', '"')

    def _check_params(self):
        return ('filename' in self.params)

    def _load(self):
        rtn = []
        for d in sent_tokenize(self.text):
            rtn.append(d.split())
        return DARelation(rtn)



class ProperNounPhraseLoader(SentenceLoader):

    def __init__(self, args):
        super(ProperNounPhraseLoader, self).__init__(args)

    def parse(self, text):
        tknzr = TweetTokenizer()
        sent = [word for word in tknzr.tokenize(text)]
        sent = nltk.pos_tag(sent)
        parsed_tokens = self.parseNoun(sent)
        noun_phrases = [ ' '.join([word[0] for word in p.leaves()])\
                         for p in parsed_tokens \
                         if isinstance(p, nltk.tree.Tree) and p.label() == 'NNG']

        noun_phrases = [re.sub(r'[^\w\s]','',n).strip()\
                         for n in noun_phrases \
                         if "'" not in n]

        return [n for n in noun_phrases if len(n) > 0 and self._is_capitalized(n)]

    def parseNoun(self, pos):
        pattern = 'NNG: {<NN|NNS|NNP>*}'
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(pos)
        return cs

    def _is_capitalized(self, word):
        return any([w[0].isupper() for w in word.split()])

    def _load(self):
        rtn = []
        for d in sent_tokenize(self.text):
            row = self.parse(d)
            if len(row) > 0:
                rtn.append(row)
        return DARelation(rtn)
        