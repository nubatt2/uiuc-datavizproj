#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 00:50:59 2018

@author: nubatt2@illinois.edu
"""

############################################
import pandas as pd
import numpy as np

import sys
import swifter
import Utils
import warnings
warnings.filterwarnings('ignore')
import time

#sentiment analysis lexicon
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
############################################
#initialize sentiment analyzer object once.
analyzer = SentimentIntensityAnalyzer()

############################################


def get_weighted_sentiment_score(verified_purchase, helpful_votes, total_votes,
                                 sentiment_score):
    weighted_votes = 0
    weighted_vp = 0

    if total_votes != 0:
        weighted_votes = helpful_votes / total_votes

    if verified_purchase.upper() == 'Y':
        weighted_vp = 1

    return (1 + weighted_votes + weighted_vp) * sentiment_score


def GetSentimentScore(sentence):
    DEFAULT_SCORE = 0
    #check if sentence is non-empty.
    # for empty return default score.
    if pd.isnull(sentence) or not sentence.strip():
        return DEFAULT_SCORE
    else:
        sentiment_scores = analyzer.polarity_scores(sentence)
        return round(sentiment_scores['compound'], 2)


@timeit
def GetProductSentimentsFor(df_data):
    print(">>>> Get raw sentiment scores. This is the slowest step!")
    df_data['sentiment_score'] = df['review_body'].swifter.apply(
        GetSentimentScore)

    print(">>>> Get weighted sentiment scores")
    df_data['weighted_sentiment_score'] = df_data.apply(
        lambda row: get_weighted_sentiment_score(row.verified_purchase, row.helpful_votes, row.total_votes, row.sentiment_score),
        axis=1)

    print(">>>> Write to file input as is + sentiment score for each item")
    df_data.to_json('../data/product_sentiments.json', orient='records')

    # Aggregated on date. Group by ProductId and Review Date. Aggregate weighted sentiment score.
    date_aggregated = df_data.groupby(
        ['product_id', 'product_title',
         'review_date'])["weighted_sentiment_score"].mean().reset_index()
    date_aggregated["aggr_weighted_sentiment_score"] = date_aggregated[
        "weighted_sentiment_score"]

    print(">>>> Write to file aggregated - date")
    date_aggregated.drop(columns=['weighted_sentiment_score']).to_json(
        '../data/product_sentiments.date_aggregated.json', orient='records')

    #aggregated on product_id
    product_aggregated = date_aggregated.groupby([
        'product_id', 'product_title'
    ])["aggr_weighted_sentiment_score"].mean().reset_index()
    product_aggregated[
        "overall_weighted_sentiment_score"] = product_aggregated[
            "aggr_weighted_sentiment_score"]

    print(">>>> Write to file aggregated - product")
    product_aggregated.drop(columns=['aggr_weighted_sentiment_score']).to_json(
        '../data/product_sentiments.product_aggregated.json', orient='records')


if __name__ == '__main__':
    print('>>>> loading dataset...')
    df = Utils.GetDataFrameFor(
        r'../data/amazon_reviews_us_Electronics_v1_00.candidates.21K.tsv')

    GetProductSentimentsFor(df)