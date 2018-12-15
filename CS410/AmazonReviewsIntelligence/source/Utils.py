'''
imports
'''
#############################
import pandas as pd
from pathlib import Path # for file path validation

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from gensim.utils import tokenize

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
nlp.max_length = 20000000
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

snowball_stemmer = SnowballStemmer('english')
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
    #Tokenize using gensim and remove stop words.
    custom_stopwords = ['i', 'me', 'he', 'she', 'him', 'her']
    nltk_stop_words = set(stopwords.words('english'))
    stopwords_integrated = nltk_stop_words.union(custom_stopwords)
    #stopwords_integrated = spacy_stopwords.union(custom_stopwords)

    candidate_tokens = [token for token in tokenize(query, deacc=True, lowercase=True, errors='ignore') if not token in stopwords_integrated and len(token) > 1 ] 
    
    #3. lemmetize
    stemmed_tokens = []
    for candidate_token in candidate_tokens:
            stemmed_tokens.append(snowball_stemmer.stem(candidate_token))
    
#     lemmed_tokens = []
#     for candidate_token in candidate_tokens:
#         lemmed_nlp = nlp(candidate_token)
#         lemmed_candidate = lemmed_nlp[0]
#         lemmed_token = lemmed_candidate.lemma_

#         # add lemmed token if it in allowed postags, otherwise, raw as is.
#         if (lemmed_candidate.pos_ in allowed_postags):
#             lemmed_tokens.append(lemmed_token)
#         else:
#             lemmed_tokens.append(candidate_token)

#     for lemmed_token in lemmed_tokens:
#         queryTokens.append(lemmed_token)

    return stemmed_tokens
