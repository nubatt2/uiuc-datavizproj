
import Utils

def GetDataForAnalysis(input_file):
    '''
    Prepare data. Filter unwanted rows + additional cleanup..
    '''
    df_data = Utils.GetDataFrameFor(input_file)
    
    # chose columns of interest, and group. Only take products witha tleast 10 reviews.
    df_grouped = df_data.groupby(by='product_id').filter(lambda x: len(x) >= 10 and len(x) < 5000)

    return df_grouped


if __name__ == '__main__':
    print('loading dataset...')

    inputFilePath = '../data/amazon_reviews_us_Electronics_v1_00.tsv.gz'
    outputFilePath = '../data/amazon_reviews_us_Electronics_v1_00.candidates.tsv'
    
    #df = Utils.GetDataFrameFor(r'../data/amazon_reviews_us_Mobile_Electronics_v1_00.tsv.gz')
    df =GetDataForAnalysis(inputFilePath)
    df.to_csv(outputFilePath, sep='\t')
    print("Complete!")
    #df_withtopics = GetTopicsFor(df)