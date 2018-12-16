#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Amazon Reviews Intelligence - Sentiments and Topics.
Created on Mon Dec 10 00:50:59 2018

@author: nubatt2@illinois.edu, mt19@illinois.edu
"""
"""
Amazon Reviews dataset downloaded form:
https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Electronics_v1_00.tsv.gz 
"""
############################################
import Utils
import sentiment_modeling
import topic_modeling
############################################

# For running this on local machine, a sample set if generated from  dataset given above.
sample_dataset = "../data/amazon_reviews_us_Electronics_v1_00.15k.sample.tsv"

#in case want to subsample.
# count is the number of product-review pairs.
# 0 or less means no sub_sample required.
sub_sample_count = 0

if __name__ == '__main__':
    df_clean = Utils.GetDataForAnalysis(sample_dataset, min_reviews=1, max_reviews=5000)
    print("shape of dataframe : {}".format(df_clean.shape))

    # in case want to further sub-sample
    if(sub_sample_count > 0):
        df_clean = df_clean.sample(sub_sample_count)

    #get sentiment scores. THis method also writes sentiment scores to file.
    df_sentiment_model = sentiment_modeling.GetProductSentimentsFor(df_clean)

    print("shape of sentiment model, dataframe : {}".format(df_sentiment_model.shape))

    #Topic modelling - overall
    print(">>> START: topic modeling!")
    df_overall_topics = topic_modeling.GetTopicsFor(df_clean)
    df_overall_topics['topics'] = df_overall_topics['Overall_Topics']

    # write overall topic score.
    df_overall_topics[['product_id', 'topics']].to_json('../data/topics-models_overall.sample.json', orient = 'records')

    # topic modeling for 
    positives_reviews_data = df_sentiment_model[df_sentiment_model['weighted_sentiment_score'] > topic_modeling.SENTIMENT_SCORE_THRESHOLD]
    negative_reviews_data  = df_sentiment_model[df_sentiment_model['weighted_sentiment_score'] < (-1 * topic_modeling.SENTIMENT_SCORE_THRESHOLD)]

    #Topic modelling - positive reviews.
    df_positive_sentiment_topics = topic_modeling.GetTopicsFor(positives_reviews_data)
    df_positive_sentiment_topics['topics'] = df_positive_sentiment_topics['Overall_Topics']
    df_positive_sentiment_topics[['product_id', 'topics']].to_json("../data/topic_models_positive.sample.json", orient='records')


    #Topic modelling - negative reviews.
    df_negative_reviews_data = topic_modeling.GetTopicsFor(negative_reviews_data)
    df_negative_reviews_data['topics'] = df_negative_reviews_data['Overall_Topics']
    df_negative_reviews_data[['product_id', 'topics']].to_json("../data/topic_models_negative.sample.json", orient='records')
    print(">>> END: topic modeling!")


