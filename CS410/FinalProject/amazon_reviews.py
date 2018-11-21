import pandas as pd
import numpy as np
import gzip


review_file = r'/Users/naseer/Documents/GitHub/uiuc-projects/CS410/FinalProject/reviews_Electronics_5.json.gz'

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF(review_file)