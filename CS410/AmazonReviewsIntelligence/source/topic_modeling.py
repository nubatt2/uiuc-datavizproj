#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 00:50:59 2018

@author: nubatt2@illinois.edu
"""

############################################
import pandas as pd

#topic modeling library.
from gensim import corpora, models
import gensim
import pyLDAvis  # visualize topic models.

# nlp library
import spacy
from spacy import displacy

import Utils
############################################
def GetTopicModelsFor(df_data):
    # chose columns of interest, and group.
    df_grouped = df_data[['product_id', 'review_body', 'review_headline']].groupby(by = 'product_id')
    product_id_lst = []
    reviews_lst = []
    for product_id, group in df_grouped:
        text = []
        for row, data in group.iterrows():
            review_body = data['review_body']
            text.append(review_body)
        
        concatenated_reviews = ' '.join(str(v) for v in text)
        
        reviews_lst.append(concatenated_reviews)
        product_id_lst.append( product_id)

    df2 = pd.DataFrame({'product_ids': product_id_lst, 'reviews': reviews_lst})
    return "1"


if __name__ == '__main__':
    print('loading dataset...')
    df = Utils.GetDataFrameFor(r'../data/amazon_reviews_us_Mobile_Electronics_v1_00.tsv.gz1')
    
    GetTopicModelsFor(df)
    print(df.head())

