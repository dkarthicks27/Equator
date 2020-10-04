from datasketch import MinHash
import time
import os
import pickle
from pandas import DataFrame as df
import numpy as np



#####################################################################################################

def operation(qry, size=5):
    array = []
    print(size)
    for y in range(0, len(qry) - size + 1):
        array.append(qry[y:y + size])
    print(array)
    stream_set = set(array)
    print(stream_set)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    return minhash


def jaccard(a, b):
    if len(a) != len(b):
        raise ValueError("Cannot compute Jaccard given MinHash with\
                        different numbers of permutation functions")
    return np.float(np.count_nonzero(a == b)) / np.float(len(a))



def similarItems(minhash, threshold):
    similarity = []
    bucket = lsh.query(minhash)
    if len(bucket) > 1:
        for value in bucket[1:]:
            sim = jaccard(minhash.hashvalues, Dict[value])
            if sim >= threshold:
                similarity.append((value, sim))


        my_df = df(similarity, columns=['duplicate_doc', 'similarity_percent'])
        with open('file.csv', 'a+') as csv_file:
            my_df.to_csv(path_or_buf=csv_file, index=False)
            similarity.clear()
        del my_df

    else:
        print("No similar items found related to the query for the given threshold")




if __name__ == '__main__':
    # Construct the argument parser


    t1 = time.time()
    args = {'filepath': r'/Users/karthickdurai/Equator/LSH/ConceptualSearch/test'}

    # so assigning variables for the input arguments
    pickle_file_directory = args['filepath']
    query = '''From: Laurel Adams [/o=cw-test/ou=first administrative group/cn=recipients/cn=laurel.adams]
To: Sara Shackleton
Subject: TR Bond Swap Confirmation

Importance:     Normal
Priority:       Normal
Sensitivity:    None

Sara,

Paul wants to know if we have any objections to the attached form of 
confirmation.  Please let me know if you have any concerns.  Thank you!  
---------------------- Forwarded by Laurel Adams/HOU/ECT on 07/31/2000 05:00 
PM ---------------------------'''

    threshold = 0

    # variable containing minhash and lsh pickle files
    minhash_location = os.path.join(pickle_file_directory, 'hash_pickle.pc')
    lsh_location = os.path.join(pickle_file_directory, 'lsh_pickle.pc')



    # checking if both these files are available and are present
    if not os.path.isdir(pickle_file_directory):
        raise ModuleNotFoundError("The input directory does not exist")


    if not os.path.isfile(minhash_location):
        raise FileNotFoundError("No file exist, Enter a valid filepath, or run indexing program with given file location")


    if not os.path.isfile(lsh_location):
        raise FileNotFoundError("No file exist, Enter a valid filepath, or run indexing program with given file location")





    # loading the Dictionary of minHash Values (not minhash objects) and lsh object
    Dict = pickle.load(open(minhash_location, 'rb'))
    lsh = pickle.load(open(lsh_location, 'rb'))


    # getting minhash of the query
    minhash = operation(query)
    similarItems(minhash=minhash, threshold=threshold)  # finding similar documents to the query


    for i in Dict:
        print(i, jaccard(Dict[i], minhash.hashvalues))
    print(f'time taken {time.time() - t1}')
