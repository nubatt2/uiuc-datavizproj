### Intelligence from Amazon Reviews - Sentiments and Topics
***

#### Introduction
Amazon is a leader of the retail industry. Multibillion transactions happen on Amazon every year.Product reviews on Amazon are an important factor in the purchase decisions made by the consumers. Poor reviews can potentially tank sales of a product. We wanted to build a tool which the product owners can use to get a pulse of their customers - get to know what they feel about the product, and what things about the product standout as positive, negative or neutral facets.

So, for this project, our goal is to mine intelligence from the product reviews. 
we mine sentiment of individual product reviews, show a trend of how the sentiments change over a pariod of time and show topics which users are talking about. Sentiments are aggregated per product so that we can show an overall score and aggregate per date which helps to show time trend. There are three categories of topics (facets) that we will present - overall, topics for positive reviews and topics for negative reviews.

As a stretch goal, we also experimented with faceted search scenario. 
For example, if the user is searching for 'best noise cancelling head phones' - search should have results with products from Bose, Sennheiser  etc. Since we get topic keywords from the topic modeling, instead of indexing product title, we indexed individual topic keywords.


In our original proposal, our goal was to run this analysis using facebook data. That is, scrape public pages of facebook - extract individual posts, do named entity extraction, sentiment analsis and topic modelling. For each extracted entity we would have shown sentiment trend and topics that users are talking about. But, we didn't get facebook approval for using their Graph API and risked our project. With the help and support of our TA, Yuncheng Wu, we were able to change dataset for our project and slightly alter the scope (amazon dataset didn't require entity extraction)

#### Description of the dataset
***
For the purpose of this project we used an existing Amazon reviews dataset made available by Amazon: https://s3.amazonaws.com/amazon-reviews-pds/readme.html 

Amazon reviews dataset is available for several product categories. we decided to use electronics dataset, with reason that products in this category are mostly familiar: https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Electronics_v1_00.tsv.gz

It's a tab separated text file without any escape characters. First line is header, and each line represents one record.

**Data Columns:**
| ColumnName|Column Description      |
|:----------|:-------------|
| marketplace|2 letter country code of the marketplace where the review was written. |
| customer_id|Random identifier that can be used to aggregate reviews written by a single author.   |
| review_id   | The unique ID of the review. |
| product_id   | The unique Product ID the review pertains to. In the multilingual dataset the reviews for the same product in different countries can be grouped by the same product_id. |
| product_parent   | Random identifier that can be used to aggregate reviews for the same product. |
| product_title   | The unique ID of the review. |
| product_category   | Broad product category that can be used to group reviews |
| star_rating   | The 1-5 star rating of the review. |
| helpful_votes   | Number of helpful votes. |
| total_votes   | Number of total votes the review received. |
| vine   | Review was written as part of the Vine program. |
| verified_purchase   | The review is on a verified purchase. |
| review_headline   | The title of the review. |
| review_body   | The review text. |
| review_date   | The date the review was written. |

Example data:
| ColumnName|Column Description      |
|:----------|:-------------|
| marketplace|US|
| customer_id|41409413|
| review_id   |R2MTG1GCZLR2DK|
| product_id   | B00428R89M |
| product_parent   |  112201306  |
| product_title   | yoomall 5M Antenna WIFI RP-SMA. |
| product_category   | Electronics |
| star_rating   | 5 |
| helpful_votes   | 0 |
| total_votes   | 0 |
| vine   | N |
| verified_purchase   | Y |
| review_headline   | Five Stars |
| review_body   | It's exactly as described. |
| review_date   | 2015-08-31. |

****
#### Package Dependencies
This project ahs several python package dependencies. Please make sure they are installed on your machine.
  - **pandas**, Python dataframes: https://pandas.pydata.org/
    <code>pip install --upgrade pandas</code>
  - **gensim**, topic modeling library:  https://radimrehurek.com/gensim/ 
    <code>pip install gensim</code>
  - **vader**, sentiment analysis lexicons: https://github.com/cjhutto/vaderSentiment 
    <code>pip install vaderSentiment</code>
  - **nltk**, NLP library, used for stopwords, stemming etc. https://www.nltk.org/
   <code>pip install -U nltk</code>
   also download it's stopwords and other data.
   <code>python -m nltk.downloader all</code>
  - **metapy** NLP library, used for hosting and querying inverted index. https://github.com/meta-toolkit/metapy
  <code>pip install metapy</code>
  - **swifter**, Package which efficiently applies any function to a pandas dataframe in the fastest available manner. https://github.com/jmcarpenter2/swifter
    <code> pip install swifter</code>
****

#### Description.
Exploratory data analysis.

##### Sentiment Analysis
talk about logic used
##### Algorithm for weighted score.
##### Topic Modeling
Using gensim topic modeling library

#### Faceted product search

#### Demo
##### Website
##### IPYNB for faceted product search.


