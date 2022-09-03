'''
Reads the data file from path
'''

import pandas as pd
path = (r"data/16pf.csv")
df = pd.read_csv(path, sep='\t')
