# Hi this is the methodology followed in this code
# It works based on LSH
# so dataSketch makes a few things easy for us-
# steps:
# 1) first open the directory, read each file converting into a set of all words in the document
# 2) second we have to create a minHashLSH object in the main function
# 3) So now we will create a minhash for each of our document
# 4) This minhash and its corresponding doc_id  are appended to an array as (key, minhashValue) pair
#    eg: [("m1", m1), ("m2", m2), ("m3", m3).....], so make sure it has some sort bulk size checking
# 5) So here we will write a function which will create a candidate pair and give us output for each document


# IMPORT STATEMENTS
import logging
import sys
from pprint import pprint

import pyodbc
from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
import re
import time
import glob


########################################################################################################################
# this section includes all the basic sql functions


def sql_connect():
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=KARTHICK\SQLEXPRESS;"
            "Database=EQUATOR;"
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


############################################################################################################################################


# This function will help us create shingles out of our text files
# ARGUMENTS: f - file, size- size of shingle
# RETURN: it returns a generator which holds the shingles
def get_shingles(f1, size):
    buf = f1.read()  # read entire file
    for y in range(0, len(buf) - size + 1):
        yield buf[y:y + size]


# Create minHash from document set and store it to the minDict dictionary
def hashLSH(stream_set, doc_id):
    minhash = MinHash(num_perm=NUM_PERMUTATION, seed=3)
    for d in stream_set:
        minhash.update(d.encode('utf8'))
    minDict[doc_id] = minhash


def create_candidate_pairs():
    similarity = {}
    for query in minDict.keys():
        array = []
        bucket = lsh.query(minDict[query])
        if len(bucket) > 1:
            _a = bucket[0]
            for value in bucket[1:]:
                _b = value
                with open(_a, errors="ignore") as f1, open(_b, errors="ignore") as f2:
                    shingle1 = set(get_shingles(f1, 3))
                    shingle2 = set(get_shingles(f2, 3))
                    jaccard_similarity = len(shingle1.intersection(shingle2))/len(shingle1.union(shingle2))
                array.append((_b, minDict[query].jaccard(minDict[_b]), jaccard_similarity))
        if len(array) != 0:
            similarity[_a] = array
    return similarity


# this is the main function
# execution starts here
if __name__ == '__main__':
    # START LOGGING
    t_initial = time.time()

    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')

    # THIS IS THE SQL CONNECTION AND QUERYING STATEMENT:
    #sql = input("Enter the sql insert statement: ")
    #connect = sql_connect()
    #k = read_sql_input(connect, sql)
    #
    #document_id = [seq[0] for seq in k]
    #fileList = [seq[1] for seq in k]
    fileList = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    fileList = fileList[:100]

    # SET THE NO. OF PERMUTATIONS
    NUM_PERMUTATION = 256
    NUM_SHINGLES = 5  # THIS IS THE NUMBER OF SHINGLES THE DOC NEEDS TO DIVIDED INTO
    minDict = {}  # This is the dictionary containing all minhash key and value

    t0 = time.time()
    # pBar = tqdm(fileList)  # just an progress meter
    i = 0
    for file in tqdm(fileList, desc="Processing"):
        with open(file, errors="ignore") as f:
            x = set(get_shingles(f, NUM_SHINGLES))
            hashLSH(stream_set=x, doc_id=file)
            i += 1
            f.close()

    print("\n")
    print(f'Shingle creation done processing time: {time.time() - t0} secs')
    print("\n")


    # Now we have to create a session for bulk insert
    # here you can set threshold as desired for qualifying for comparison
    t1 = time.time()
    # FEEL FREE TO CHANGE THE VALUES OF WEIGHTS HERE THEY ARE
    # THE IMPORTANCE GIVEN TO MINIMISING FALSE POSITIVE OR FALSE NEGATIVE
    # FALSE POSITIVE: SOMETHING IS NOT POSITIVE BUT STILL INCLUDED
    # FALSE NEGATIVE: SOMETHING IS POSTIVE BUT DECLARED AS POSITIVE
    # IF WE WANT MORE PRECISION i.e. identify accurate results and not flag original doc as dup even missing some original though
    # WHILE BY SETTING FALSE NEGATIVE AS MIN AS POSSIBLE we allow duplicate values as well as non dup ones
    lsh = MinHashLSH(threshold=0.70, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(minDict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=minDict[key])

    print("\n")
    print(f'LSH processing done time taken is {time.time() - t1} secs')
    print("\n")

    print("Finding out similar items...")
    sim = create_candidate_pairs()
    print("\n")

    pprint(sim)
    print("\n\n")
    print(f"Total processing time is {time.time() - t_initial} secs")

