import pickle
import os
import argparse
import time
from sklearn.metrics.pairwise import cosine_similarity
from pandas import DataFrame as df


def pipeline(queryString, lsi, tfidfVectorizer):
    vector = tfidfVectorizer.transform(queryString)
    reduced_vec = lsi.transform(vector)
    return reduced_vec

def cosineSimilarity(query_vec, vec, thresh, output, doc_id):
    similarity = []
    storage = os.path.join(output, 'conceptual_result.csv')
    sims = cosine_similarity(query_vec, vec)

    for pos, element in zip(doc_id, sims[0]):
        if element >= thresh:
            similarity.append((pos, element))

    my_df = df(similarity, columns=['document_id', 'similarity_percent'])
    with open(storage, 'a+') as csv_file:
        my_df.to_csv(path_or_buf=csv_file, index=False)
        similarity.clear()
    del my_df



if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-f", "--filepath", required=True, help="pickled directory file path", metavar="")
    ap.add_argument("-q", "--query", required=True, help="conceptual search query as string", metavar="", nargs='*')
    ap.add_argument("-t", "--threshold", required=True, help="threshold for conceptual search", metavar="", nargs=1,
                    type=int)
    ap.add_argument("-o", "--finalResultPath", required=True, help="directory where final result is to be saved", metavar="")
    args = vars(ap.parse_args())

    t1 = time.time()

    # so assigning variables for the input arguments
    pickle_file_directory = args['filepath']
    query = [' '.join(args['query'])]
    threshold = args['threshold']
    output_path = args['finalResultPath']

    print('importing the required documents\n')
    # so we need three important objects
    # 1. doc_id, filepath array is needed to iterate through it and compare for cosine similarity
    # 2. tfidf vectorizer is required to convert the query string into a vector
    # 3. lsi model is required to reduce the dimension of the vector to the default value
    # 4. lsi truncated vector is required so that we can actually build cosine similarity

    docPath = os.path.join(pickle_file_directory, 'doc_id.pc')
    tfidfVectorizerPath = os.path.join(pickle_file_directory, 'tfidfVectorizer.pc')
    svdPath = os.path.join(pickle_file_directory, 'svd.pc')
    vectorsPath = os.path.join(pickle_file_directory, 'vector.pc')

    # checking if both these files are available and are present
    if not os.path.isdir(pickle_file_directory):
        raise ModuleNotFoundError("The input directory does not exist")

    if not os.path.isfile(svdPath):
        raise FileNotFoundError(
            "No file exist, Enter a valid filepath, or run indexing program with given file location")

    if not os.path.isfile(docPath):
        raise FileNotFoundError(
            "No file exist, Enter a valid filepath, or run indexing program with given file location")

    if not os.path.isfile(tfidfVectorizerPath):
        raise FileNotFoundError(
            "No file exist, Enter a valid filepath, or run indexing program with given file location")

    if not os.path.isfile(vectorsPath):
        raise FileNotFoundError(
            "No file exist, Enter a valid filepath, or run indexing program with given file location")

    # Now loading the models and vectors to the memory

    doc = pickle.load(open(docPath, 'rb'))
    tfidf = pickle.load(open(tfidfVectorizerPath, 'rb'))
    svd = pickle.load(open(svdPath, 'rb'))
    vectors = pickle.load(open(vectorsPath, 'rb'))

    # we need to convert the query file into final resultant vector
    # building the required pipeline query -----> tfidf ------> LSI ------> reduced vector

    queryVec = pipeline(query, svd, tfidf)
    cosineSimilarity(queryVec, vectors, threshold, output_path, doc_id=doc)

    print(f'Total time taken is {time.time() - t1}')
