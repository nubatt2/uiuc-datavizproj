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

import warnings
warnings.filterwarnings('ignore')

import time
############################################

MIN_REVIEWS = 10


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


@timeit
def GetDataForModeling(df_data):
    '''
    Choses columns of interest and create one row for each product - all reviews.
    '''
    # chose columns of interest, and group. Only take products witha tleast 10 reviews.
    # df_grouped = df_data[[
    #     'product_id', 'review_body'
    # ]].groupby(by='product_id').filter(lambda x: len(x) >= 10)
    
    # blacklisted product.
    df_data = df_data[df_data['product_id'] != 'B003L1ZYYM']
    df_candidate = df_data[['product_id', 'review_body']].groupby(by='product_id')['review_body'].apply(lambda x:' '.join(str(v) for v in x)).reset_index()
    
    # return joined
    # df_candidate = df_grouped.groupby(by='product_id')['review_body'].apply(lambda x:' '.join(str(v) for v in x)).reset_index()
    return df_candidate

    # product_id_lst = []
    # reviews_lst = []
    # for product_id, group in df_grouped:
    #     text = []
    #     for row, data in group.iterrows():
    #         review_body = data['review_body']
    #         text.append(review_body)

    #     concatenated_reviews = ' '.join(str(v) for v in text)

    #     reviews_lst.append(concatenated_reviews)
    #     product_id_lst.append(product_id)

    # return pd.DataFrame({
    #     'product_ids': product_id_lst,
    #     'reviews': reviews_lst
    # })


def GetCandidateTexts(input_string):
    query_strippedhtml = Utils.strip_tags(input_string)
    return Utils.GetQueryTokens(query_strippedhtml)


def TrainAndPredictTopicModel(texts):
    NUMBER_OF_WORDS_PER_TOPIC = 20
    # print(type(texts))
    candidate_text = texts
    if (len(candidate_text) < 3):
        return

    # Create Dictionary
    id2word = corpora.Dictionary([candidate_text])

    # Create Corpus
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in [candidate_text]]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=2,
        random_state=100,
        update_every=1,
        chunksize=100,
        passes=10,
        alpha='auto',
        per_word_topics=True)

    #get keywords for the first topic.
    topics_list = lda_model.show_topic(0, NUMBER_OF_WORDS_PER_TOPIC)
    return topics_list


@timeit
def GetTopicsFor(df_data):
    print(">>>> Combine and get candidates for topic modelling!")
    products_to_topicalize = GetDataForModeling(df_data)

    print("Number of products to get topics for {}".format(len(products_to_topicalize)))
    ## write to file for intermediate storage
    products_to_topicalize.to_json("dataformodeling.json", orient='records')

    # tokenize, cleanup, lemmitize text.
    print(">>>> Tokenize sentences!")
    products_to_topicalize['candidate_texts'] = products_to_topicalize['review_body'].apply(GetCandidateTexts)

    ## write to file for intermediate storage
    products_to_topicalize[['product_id', 'candidate_texts']].to_json("tokenized.json", orient='records')

    print(">>>> Train topic model!")
    products_to_topicalize['Overall_Topics'] = products_to_topicalize['candidate_texts'].apply(TrainAndPredictTopicModel)

    return products_to_topicalize


if __name__ == '__main__':
    print('>>>> loading dataset...')
    #df = Utils.GetDataFrameFor(r'../data/amazon_reviews_us_Mobile_Electronics_v1_00.tsv.gz')
    df = Utils.GetDataFrameFor(r'../data/amazon_reviews_us_Electronics_v1_00.candidates.21K.tsv')

    df_withtopics = GetTopicsFor(df)
    #df_withtopics = GetTopicsFor(df)

    # orient is important, tells how to index json.
    df_withtopics[['product_id', 'Overall_Topics']].to_json(
        "topic_models.json", orient='records')
    print("##COMPLETE!!!!! ###")
    #print(df_withtopics.head())