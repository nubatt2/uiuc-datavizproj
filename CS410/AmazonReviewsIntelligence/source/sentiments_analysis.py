#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 00:50:59 2018

@author: mtripath
"""

import pandas as pd
import numpy as np
import sys

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def load_dataset():
    # this is the dataset downloaded from AMZN directly.
    mobile_electronics_review_file = '../data/amazon_reviews_us_Mobile_Electronics_v1_00.tsv.gz'
    df_me = pd.read_table(mobile_electronics_review_file, error_bad_lines=False)
    #df_me.head()
    print(list(df_me))
    #print(mod_df.sort_values(by=['product_id'])[1:10])
    return df_me


def write_json_file(df, file_name, orientation):
    df.to_json(file_name, orient = orientation)


def get_weighted_sentiment_score(verified_purchase, helpful_votes, total_votes, sentiment_score):
    weighted_votes = 0
    weighted_vp = 0
    
    if total_votes != 0:
        weighted_votes = helpful_votes/total_votes
    
    if verified_purchase.upper() == 'Y':
        weighted_vp = 1
        
    return (1 + weighted_votes + weighted_vp) * sentiment_score
    

def generate_sentiment_score(df_me):
    # Starting with small dataset
    #df_me_small = df_me[1:1000]
    # Removing products with less than 10 reviews (Sort, Group then Filter)
    #grouped_product_id = df_me_small.sort_values(by=['product_id']).groupby('product_id').filter(lambda x: len(x) >= 10)
    # This is full dataset
    # Removing products with less than 10 reviews (Sort, Group then Filter)
    grouped_product_id = df_me.sort_values(by=['product_id']).groupby('product_id').filter(lambda x: len(x) >= 10)
    #print(grouped_product_id)
    
    df_vs = pd.DataFrame()
    analyzer = SentimentIntensityAnalyzer()
    #review_body_index = df_vs.columns.get_loc("review body")
    #print(review_body_index)
    #for name,group in grouped_product_id_filtered:
        #print(name)
        #print(group['review_body'])
    
    # Calculate sentiment score for all product reviews
    for row in grouped_product_id.itertuples():
        try:
            vs = analyzer.polarity_scores(row[14])
            #print("{:-<65} {}".format(row[14], str(vs)))
            #print(vs['compound'])
            # Store sentiment score and weighted sentiment score in dataframe
            curr_data = [row[4], row[6], row[9], row[10], row[12], row[13], row[14], row[15], vs['compound'], get_weighted_sentiment_score(row[12], row[9], row[10], vs['compound'])]
            curr_df = pd.DataFrame([curr_data], columns = ['product_id', 'product_title', 'helpful_votes', 'total_votes', 'verified_purchase', 'review_headline', 'review_body', 'review_date', 'sentiment_score', 'weighted_sentiment_score' ])
            #print(row[0])
            #print(curr_data)
            df_vs = df_vs.append(curr_df, ignore_index=True)
            #print(df_vs)
        except AttributeError as err:
            print("Attribute error: {0}".format(err))
            print(row[14])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(row[14])
            
    # Write sentiment scores along with product data to json file (TABLE 1)
    write_json_file(df_vs, '../data/product_sentiments.json', 'records')
    print('Done with Table 1 - sentiment scores along with product data')
    
    # Aggregated on date. Group by ProductId and Review Date. Aggregate weighted sentiment score.
    grouped_product_date = df_vs.sort_values(by=['product_id']).groupby(['product_id', 'review_date'])
    aggregated_score_date = grouped_product_date['weighted_sentiment_score'].agg(np.mean)
    #print(aggregated_score_date)
    
    # Dataset having aggregated weighted sentiment score for date for product
    df_aggregated_score_date = pd.DataFrame()
    for name in aggregated_score_date.index:
        #print(name)
        #print(aggregated_score_date.loc[name])
        curr_aggr_data = [name[0], name[1], aggregated_score_date.loc[name]]
        curr_aggr_df = pd.DataFrame([curr_aggr_data], columns = ['product_id', 'review_date', 'aggr_weighted_sentiment_score'])
        df_aggregated_score_date = df_aggregated_score_date.append(curr_aggr_df, ignore_index=True)
    #print(df_aggregated_score_date)
    # Write aggregated weighted sentiment score along with product and review date to json file (TABLE 2)
    write_json_file(df_aggregated_score_date, '../data/product_sentiments_aggregated_dates.json', 'records')
    print('Done with Table 2 - aggregated weighted sentiment score along with product and review date')
    
    # Aggregrate for product
    grouped_product = df_aggregated_score_date.sort_values(by=['product_id']).groupby('product_id')
    aggregated_score_overall = grouped_product['aggr_weighted_sentiment_score'].agg(np.mean)
    #print(aggregated_score_overall)
    
    # Dataset having overall aggregated weighted sentiment score for product
    df_aggregated_score_overall = pd.DataFrame()
    for name in aggregated_score_overall.index:
        #print(name)
        #print(aggregated_score_overall.loc[name])
        curr_aggr_overall_data = [name, aggregated_score_overall.loc[name]]
        curr_aggr_overall_df = pd.DataFrame([curr_aggr_overall_data], columns = ['product_id', 'overall_weighted_sentiment_score'])
        df_aggregated_score_overall = df_aggregated_score_overall.append(curr_aggr_overall_df, ignore_index=True)
    #print(df_aggregated_score_overall)
    # Write overall aggregated weighted sentiment score along with product to json file (TABLE 3)
    write_json_file(df_aggregated_score_overall, '../data/product_sentiments_aggregated_overall.json', 'records')
    print('Done with Table 3 - overall aggregated weighted sentiment score along with product')
    
    
if __name__ == '__main__':
    print('loading dataset...')
    df_me = load_dataset()
    generate_sentiment_score(df_me)
