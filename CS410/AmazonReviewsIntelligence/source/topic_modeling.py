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

# making apply fast!
import swifter

import Utils

import warnings
warnings.filterwarnings('ignore')

############################################
MIN_REVIEWS = 10
SENTIMENT_SCORE_THRESHOLD  = 1

def GetDataForModeling(df_data):
    '''
    Choses columns of interest and create one row for each product - all reviews.
    '''
    # blacklisted product.
    #df_data = df_data[df_data['product_id'] != 'B003L1ZYYM']
    df_candidate = df_data[['product_id', 'review_body']].groupby(by='product_id')['review_body'].apply(lambda x:' '.join(str(v) for v in x)).reset_index()    
    return df_candidate


def GetCandidateTexts(input_string):
    query_strippedhtml = Utils.strip_tags(input_string)
    return Utils.GetQueryTokens(query_strippedhtml)


def TrainAndPredictTopicModel(texts):
    '''
    This mehod trains a LDA model
    Number of topics fixed to 1
    Number of words per topic fixed to 20

    These thresholds based on offline eval.
    '''
    NUMBER_OF_WORDS_PER_TOPIC = 20
    
    #candidates.
    candidate_text = texts
    #just a guard against unexpected!
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

def GetTopicsFor(df_data):
    print(">>>> Combine and get candidates for topic modelling!")
    products_to_topicalize = GetDataForModeling(df_data)

    print("Number of products to get topics for {}".format(len(products_to_topicalize)))
    ## write to file for intermediate storage
    #products_to_topicalize.to_json("dataformodeling.json", orient='records')

    # tokenize, cleanup, lemmitize text.
    print(">>>> Tokenize sentences!")
    products_to_topicalize['candidate_texts'] = products_to_topicalize['review_body'].swifter.apply(GetCandidateTexts)

    ## write to file for intermediate storage
    #products_to_topicalize[['product_id', 'candidate_texts']].to_json("tokenized.json", orient='records')

    print(">>>> Train topic model!")
    products_to_topicalize['Overall_Topics'] = products_to_topicalize['candidate_texts'].swifter.apply(TrainAndPredictTopicModel)

    return products_to_topicalize


if __name__ == '__main__':
    print('>>>> loading dataset...')    
    # read sentiment data for positive and negative labels.
    product_sentiment_data = pd.read_json(r'../data/product_sentiments.json')
    positives_reviews_data = product_sentiment_data[product_sentiment_data['weighted_sentiment_score'] > 0.5]
    negative_reviews_data = product_sentiment_data[product_sentiment_data['weighted_sentiment_score'] < -0.5]
    
    
    print(">>>> START: POSITIVE topic modelling")
    df_withtopics = GetTopicsFor(positives_reviews_data)
    #df_withtopics = GetTopicsFor(df)
    
    df_withtopics['Positive_Topics'] = df_withtopics['Overall_Topics']
    df_withtopics.drop(columns=['Overall_Topics']).to_json("topic_models.positive.21K.json", orient='records')
    print(">>>> END: POSITIVE topic modelling")
    

    print(">>>> START: NEGATIVE topic modelling")
    df_withtopics = GetTopicsFor(negative_reviews_data)
    #df_withtopics = GetTopicsFor(df)
    
    df_withtopics['Negative_Topics'] = df_withtopics['Overall_Topics']
    df_withtopics.drop(columns=['Overall_Topics']).to_json("topic_models.negative.21K.json", orient='records')
    print(">>>> END: NEGATIVE topic modelling")
          
          
    