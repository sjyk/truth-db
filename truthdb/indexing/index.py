import pandas as pd
import sys

class Index():

    def __init__(self, generator):
        self.generator = generator
        self.performance_stats = []
        self.statement_map = None
        self.statement_imap = None
        self.mention_table = None


    def build(self, gen_params):
        import datetime
        now = datetime.datetime.now()

        gen = self.generator(gen_params)
        self.performance_stats.append(gen.load())
        self.statement_map = {statement:index for index,statement in enumerate(gen.data)}
        self.statement_imap = {index: statement for index,statement in enumerate(gen.data)}
        
        mention_table = []
        for stat in gen.data:
            mentions = stat.getAllValidMentions()

            for m in mentions:
                mention_table.append((m, self.statement_map[stat], m.rarity))

        self.mention_table = pd.DataFrame(mention_table, columns=['mention', 'statement_id', 'rarity'])

        elapsed = (datetime.datetime.now()-now).total_seconds()
        size = sys.getsizeof(mention_table) + sys.getsizeof(self.statement_map)
        return {'time': elapsed, 'size': size, 'label': 'indexing'}


"""
def compare(index1, index2, threshold=3):
    merged_df = index1.mention_table.merge(index2.mention_table, on='mention')
    print(merged_df)
    #inconsistencies = (merged_df['sentiment_x'] != merged_df['sentiment_y'])
    #merged_df = merged_df[inconsistencies]

    statements = merged_df.groupby(["statement_id_x","statement_id_y"]).size()
    thresh = (statements > threshold)
    incons = [(index1.statement_imap[i],index2.statement_imap[j]) for i,j in statements[thresh].index.tolist()]
    
    return incons
"""


