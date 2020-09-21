import argparse
from datasketch import MinHash
import time
import os
import pyodbc
import sys
import pickle
from pandas import DataFrame as df
import numpy as np



########################################################################################################################
# this section includes all the basic sql functions


def sql_connect(server, database):
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            f"Server={server};"
            f"Database={database};"
            "Trusted_Connection=yes;"
        )
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
        return "unable to connect"
    else:
        return conn


def close_sql_connection(connection):
    try:
        connection.close()
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
        return 0
    else:
        return 1


def read_sql_input(connection, read_statement):
    try:
        cursor = connection.cursor()
        cursor.execute(read_statement)
        # fetchall is risky as all the rows are loaded on to memory, so it is better to fetch one row at a time
        # rows = cursor.fetchall() must be avoided in most cases
        # instead we can use a while loop like this and give the exit condition as row being empty
        array = []
        for row in cursor:
            array.append(row)
        return array
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
    finally:
        connection.close()


def insert_sql(connection, insert_statement, values):
    try:
        cursor = connection.cursor()
        cursor.executemany(insert_statement, values)
        cursor.commit()
    except:
        print("Oops!", sys.exc_info(), "occured.\n")
    finally:
        connection.close()


def truncate_sql_table(connection, sql_statement):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        cursor.commit()
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
    finally:
        connection.close()

#####################################################################################################

def operation(qry, size=5):
    array = []
    for y in range(0, len(qry) - size + 1):
        array.append(qry[y:y + size])
    stream_set = set(array)
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
    ap = argparse.ArgumentParser()


    # Add the arguments to the parser
    ap.add_argument("-f", "--filepath", required=True, help="pickled directory file path", metavar="")
    ap.add_argument("-q", "--query", required=True, help="conceptual search query as string", metavar="", nargs='*')
    ap.add_argument("-t", "--threshold", required=True, help="threshold for conceptual search", metavar="", nargs=1, type=int)
    args = vars(ap.parse_args())

    t1 = time.time()


    # so assigning variables for the input arguments
    pickle_file_directory = args['filepath']
    query = ' '.join(args['query'])
    threshold = args['threshold']

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

    print(f'time taken {time.time() - t1}')
