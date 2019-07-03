import pandas as pd
import sys

class Index():

    def __init__(self, generator, analyzer):
        self.generator = generator
        self.analyzer = analyzer
        self.performance_stats = []
        self.statement_map = None
        self.mention_table = None

    def build(self, gen_params, an_params):
        import datetime
        now = datetime.datetime.now()

        gen = self.generator(gen_params)
        self.performance_stats.append(gen.load())
        self.statement_map = {statement: index for index,statement in enumerate(gen.data)}
        
        mention_table = []
        an = self.analyzer(gen.data, an_params)
        self.performance_stats.append(an.run())
        for stat, sent in an.result:
            mentions = stat.getAllValidMentions()

            for m in mentions:
                mention_table.append((m, self.statement_map[stat], sent))

        self.mention_table = pd.DataFrame(mention_table, columns=['mention', 'statment_id', 'sentiment'])

        elapsed = (datetime.datetime.now()-now).total_seconds()
        size = sys.getsizeof(mention_table) + sys.getsizeof(self.statement_map)
        return {'time': elapsed, 'size': size, 'label': 'indexing'}


