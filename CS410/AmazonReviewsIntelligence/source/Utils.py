'''
imports
'''
#############################
import pandas as pd
from pathlib import Path # for file path validation

# nlp library
import spacy
from spacy import displacy
import en_core_web_sm

# html parser.
from HtmlStrip import MLStripper
#############################
tokenize_blacklist = ['PUNCT', 'SPACE']
# perf optimization. don't need ner and parser.
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner', 'tagger', 'entityrecognizer'])
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
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


def GetQueryTokens(query, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    queryTokens = []

    #load spacy doc.
    doc_sp = nlp(query)

    #1. Tokenize
    tokens = [
        token.text.lower() for token in doc_sp
        if token.pos_ not in tokenize_blacklist
    ]

    #2. remove stop words
    stopped_tokens = [
        token for token in tokens if not token in spacy_stopwords
    ]

    #3. lemmetize
    # lemmed_tokens = []
    # for stopped_token in stopped_tokens:
    #     lemmed_nlp = nlp(stopped_token)
    #     lemmed_token = lemmed_nlp[0].lemma_

    #     # add lemmed token if it in allowed postags, otherwise, raw as is.
    #     if (lemmed_nlp.pos_ in allowed_postags):
    #         lemmed_token.append(lemmed_token)
    #     else:
    #         lemmed_token.append(stopped_token)

    # for lemmed_token in lemmed_tokens:
    #     queryTokens.append(lemmed_token)

    return stopped_tokens
