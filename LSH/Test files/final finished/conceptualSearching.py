import argparse
import hashlib
import pickle
import os
from pandas import DataFrame as df


def jaccard(a, b):
    """This function is used to find the jaccard similarity between two documents
        returns float (range is from 0.0 to  1.0)
    """
    return len(a.intersection(b))/len(a)



def similar(qry, index):
    """
    :param qry: set of hash values
    :param index: dictionary (key: documentID, value: hashValue of that document)
    :return: None
    """
    similarity = []
    for i in Dict:
        sims = jaccard(qry, index)
        if sims >= threshold:
            similarity.append((i, sims))

    my_df = df(similarity, columns=['document', 'similarity_percent'])
    with open(os.path.join(filePath, 'file.csv'), 'a+') as csv_file:
        my_df.to_csv(path_or_buf=csv_file, index=False)
        similarity.clear()
    del my_df



def findHash(string):
    """
    converting the input string into set of hashValues
    :param string: str
    :return: set of hexadecimals
    """
    stream_set = set(string)
    final = set()
    for word in stream_set:
        m = hashlib.sha256()
        m.update(word.encode('utf-8'))
        final.add(m.hexdigest())
    return final




if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-f", "--filepath", required=True, help="pickled directory file path", metavar="")
    ap.add_argument("-q", "--query", required=True, help="conceptual search query as string", metavar="", nargs='*')
    ap.add_argument("-t", "--threshold", required=True, help="threshold for conceptual search", metavar="", nargs=1,
                    type=int)


    args = vars(ap.parse_args())
    filePath = args['filepath']
    buf = args['query']
    threshold = args['threshold']





    if not os.path.isdir(filePath):
        raise ModuleNotFoundError('This module does not exist\
                                   please provide a valid directory or rerun the index program')
    # Loading both index dictionary and the stopwords

    if not os.path.isfile(os.path.join(filePath, 'index.pc')):
        raise FileNotFoundError('File not found re run the index program. Expecting the same filepath supplied\
                                to Indexing program')
    with open(os.path.join(filePath, 'index.pc'), 'rb') as f:
        Dict = pickle.load(f)

    if not os.path.isfile(os.path.join(filePath, 'stopwords.pc')):
        raise FileNotFoundError('File not found re run the index program. Expecting the same filepath supplied\
                                to Indexing program')
    stopWords = pickle.load(open(os.path.join(filePath, 'stopwords.pc'), 'rb'))




    # preparing the query
    # cleaning the query and hashing the query
    buf = [word for word in buf.lower().split() if word not in stopWords]
    if len(buf) == 0:
        raise ValueError('The length of the input query after removing stopwords is 0\
                         length of the string must be at least one')
    query = findHash(buf)


    # performing query to see matching documents

    similar(query, Dict)
