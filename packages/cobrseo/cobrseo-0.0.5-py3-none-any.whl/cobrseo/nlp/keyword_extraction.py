

raise NotImplementedError("To be completed in future versions ;)")


import pandas as pd
import pke
import logging


# ===================================
#     Adding logger to the module
# ===================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s : %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

file_handler = logging.FileHandler('log.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# ===================================




def get_kw_single_rank(content, lang='en', pos={'NOUN'}, window=10, 
        top_n=30, threshold=0, ngram=(1,4)):

    extractor = pke.unsupervised.SingleRank()
    extractor.load_document(input=content, language=lang, normalization=None)
    extractor.candidate_selection(pos=pos)
    extractor.candidate_weighting(window=window, pos=pos)
    keywords = extractor.get_n_best(n=top_n)

    keywords = [k for k in keywords if (k[1] > threshold)]
    
    filtered_keywords = []
    for k in keywords:
        words = k[0].split()
        unique_words = list(set(words))

        #  delete duplicated words in a keyword
        if len(words) != len(unique_words):
            kk = ' '.join(unique_words)
        else:
            kk = k
        
        #  filter out by ngram size
        if (len(kk[0].split()) >= ngram[0] and len(kk[0].split()) <= ngram[1]):
            filtered_keywords.append(kk)
    
    result = {}
    result['keyword'] = [k[0] for k in filtered_keywords]
    result['score'] = [k[1] for k in filtered_keywords]
    
    df = pd.DataFrame(data=result)
    df = df.drop_duplicates(subset=['keyword'])
    df = df.sort_values(by='score', ascending=False)
    
    if verbose:
        print(f'Found {len(df)} keywords.')
    
    return df.to_dict(orient='list')