'''
imports
'''
#############################
import pandas as pd
# for file path validation
from pathlib import Path

# nlp library
import spacy
from spacy import displacy

# html parser.
from HtmlStrip import MLStripper

#############################

def GetDataFrameFor(filePath):
    my_file = Path(filePath)
    try:
        my_file.resolve()
    except FileNotFoundError:
        # doesn't exist, raise an exception!
        raise FileNotFoundError(
            "{} does not exist. Please check file path.".format(filePath))
    else:
        #let's skip bad lines in the file.
        return pd.read_table(filePath, error_bad_lines=False)


def FilterReviewsLessThanThreshold(df_data):
    # Removing products with less than 10 reviews (Sort, Group then Filter)
    MIN_REVIEWS = 10

    return df_data.sort_values(by=['product_id']).groupby('product_id').filter(
        lambda x: len(x) >= MIN_REVIEWS)


def strip_tags(html):
    '''
    removes html script tags from given input.
    '''
    s = MLStripper()
    s.feed(html)
    return s.get_data()