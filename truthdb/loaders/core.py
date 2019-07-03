'''This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

Truth DB works by identifying ``entities'' in statements and correlating
them across datasets. We call these entities "mentions", which are formally
boolean conditions. The core.py module defines the basic abstract classes
Statement and Mention.  
'''


class Statement():
    '''A statement is the basic abstract data type in Truth DB. It can be
    a sentence or it can be a database tuple, or any other object. Inheritting
    classes have to impelement getData, getRawData, and getAllValidMentions.
    '''

    def getData(self):
        '''getData() return the processed data contained in this statement.
        '''
        raise NotImplemented("This statement has not been defined with data")

    def getRawData(self):
        '''getRawData() return the raw data contained in this statement.
        '''
        raise NotImplemented("This statement has not been defined with raw data")

    def getAllValidMentions(self):
        '''Returns all the valid mentions relevant to this statement.
        '''
        return set()

    def hasMention(self, mention):
        '''Tests to see if a mention is valid on this data
        '''
        return mention.test(self.getData())


    def __eq__(self, other):
        return (other.getRawData() == self.getRawData())

    def __hash__(self):
        return hash(self.getRawData())

    def __str__(self):
        return str({'Statement': self.getRawData()})

    __repr__ = __str__



class Mention():
    '''A mention is a boolean condition that tests the existence
    of an entity in a statement.
    '''

    def test(self):
        return False



class Generator():
    '''Generator is the basic data loading class in TruthDB.
    '''

    def __init__(self, iterator):
        '''
        A generator takes an input iterator and loads from that
        iterator.
        '''
        self.iterator = iterator
        self.data = None


    def prot_load(self):
        '''The prot_load method extracts Statements from the iterator it
        returns a set of Statements. This method should not be called from
        the outside.
        '''
        raise NotImplemented("prot_load not impelemented")

    def load(self):
        ''' The load method stores the extracted data in self.data and
        returns diagnostic information.
        '''
        import datetime
        now = datetime.datetime.now()
        self.data = self.prot_load()
        elapsed = (datetime.datetime.now()-now).total_seconds()
        size = len(self.data)
        return {'time': elapsed, 'extracted': size, 'label': 'loading'}




class SentimentAnalyzer():

    def __init__(self, data, args={}):
        self.data = data
        self.args = args
        self.result = None

    def batchAnalyze(self):
        raise NotImplemented("batchAnalyze() not impelemented")


    def run(self):
        import datetime
        now = datetime.datetime.now()
        self.result = self.batchAnalyze()
        elapsed = (datetime.datetime.now()-now).total_seconds()
        size = len(self.result)
        return {'time': elapsed, 'extracted': size, 'label': 'sentiment'}





