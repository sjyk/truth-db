'''This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This module defines the primitives for manipulating textual documents. 

CORE_NLP_PATH = '/Users/sanjaykrishnan/Documents/fact-checking/stanford-corenlp-full-2018-10-05'
'''

from .core import Loader
from truthdb.exec.rel import DARelation
import pandas as pd



class PandasLoader(Loader):

    def __init__(self, args):
        super(PandasLoader, self).__init__(args)

    def _check_params(self):
        return isinstance(self.params, pd.DataFrame)

    def _load(self):
        columns = self.params.columns
        N, _ = self.params.shape

        rtn = []
        for i in range(N):
            row = self.params.iloc[i]
            rtn.append([(c,row[c]) for c in columns])

        return DARelation(rtn)
        