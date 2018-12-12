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


def GetDataForModeling(df_data):
    '''
    Choses columns of interest and create one row for each product - all reviews.
    '''
    # chose columns of interest, and group.
    df_grouped = df_data[['product_id', 'review_body',
                          'review_headline']].groupby(by='product_id')
    product_id_lst = []
    reviews_lst = []
    for product_id, group in df_grouped:
        text = []
        for row, data in group.iterrows():
            review_body = data['review_body']
            text.append(review_body)

        concatenated_reviews = ' '.join(str(v) for v in text)

        reviews_lst.append(concatenated_reviews)
        product_id_lst.append(product_id)

    return pd.DataFrame({
        'product_ids': product_id_lst,
        'reviews': reviews_lst
    })


def GetCandidateTexts(input_string):
    query_strippedhtml = Utils.strip_tags(input_string)
    return Utils.GetQueryTokens(query_strippedhtml)


def GetTopicModelsFor(df_data):
    products_to_topicalize = GetDataForModeling(df_data)

    # tokenize, cleanup, lemmitize text.
    products_to_topicalize['candidate_texts'] = products_to_topicalize[
        'reviews'].apply(GetCandidateTexts)

    candidate_text = products_to_topicalize['candidate_texts']

    # Create Dictionary
    id2word = corpora.Dictionary(candidate_text)

    # Create Corpus
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in candidate_text]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=5,
        random_state=100,
        update_every=1,
        chunksize=100,
        passes=10,
        alpha='auto',
        per_word_topics=True)

    ## ideal DF - productId, topics.
    return products_to_topicalize


if __name__ == '__main__':
    print('loading dataset...')
    df = Utils.GetDataFrameFor(
        r'../data/amazon_reviews_us_Mobile_Electronics_v1_00.tsv.gz1')

    GetTopicModelsFor(df)
    print(df.head())