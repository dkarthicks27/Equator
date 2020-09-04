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
import os
import pickle
import sys
from glob import glob
from itertools import repeat
import pyodbc
from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
import time
import multiprocessing as mp
from pandas import DataFrame as df
import argparse


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


# This function will run the shingle creation and Minhash operation
# ARGUMENTS: f - file, d- Manager Dictionary which is shared resource
# RETURN: None

# def operation(d, f):
#     with open(f, errors="ignore") as f1:
#         buf = f1.read()  # read entire file
#     array = []
#     for y in range(0, len(buf) - 5 + 1):
#         array.append(buf[y:y + 5])
#     stream_set = set(array)
#     minhash = MinHash(num_perm=NUM_PERMUTATION)
#     for x in stream_set:
#         minhash.update(x.encode('utf8'))
#     try:
#         d[f] = minhash
#     finally:
#         pass

def operation(d, file):
    size = 5
    with open(file, errors="ignore") as f1:
        buf = f1.read()  # read entire file
    array = []
    for y in range(0, len(buf) - size + 1):
        array.append(buf[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    d[file] = minhash


# this is the main function
# execution starts here
if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-o", "--output", required=True)
    args = vars(ap.parse_args())

    # START LOGGING
    t_initial = time.time()
    k = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    k = k[:50]
    NUM_PERMUTATION = 256

    # This is the shared Dictionary
    minDict = mp.Manager().dict()

    # creating an iterable which will be used in our case
    iterable = zip(repeat(minDict, len(k)), k)

    print(f'{time.time() - t_initial} secs is taken for initialisation')
    print("shingle processing starts....")
    # Mapping each operation to iterable list

    with mp.Pool() as pool:
        pool.starmap(operation, iterable)

    print("\n")
    print(f'Shingle creation and hashing done time: {time.time() - t_initial} secs')
    print("\nInitiating LSH....")
    location = os.path.join(args['output'], 'pickle.pc')

    with open(location, 'wb') as f:
        pickle.dump(minDict, f)

    print(f'pickle file location: {location}')
    # Now we have to create a session for bulk insert
    # here you can set threshold as desired for qualifying for comparison

    # FEEL FREE TO CHANGE THE VALUES OF WEIGHTS HERE THEY ARE
    # THE IMPORTANCE GIVEN TO MINIMISING FALSE POSITIVE OR FALSE NEGATIVE
    # FALSE POSITIVE: SOMETHING IS NOT POSITIVE BUT STILL INCLUDED
    # FALSE NEGATIVE: SOMETHING IS POSTIVE BUT DECLARED AS POSITIVE
    # IF WE WANT MORE PRECISION i.e. identify accurate results and not flag original doc as dup even missing some original though
    # WHILE BY SETTING FALSE NEGATIVE AS MIN AS POSSIBLE we allow duplicate values as well as non dup ones

    # lsh = MinHashLSH(threshold=0.90, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    # with lsh.insertion_session() as session:
    #     for key in tqdm(minDict.keys(), desc="LSH processing"):
    #         session.insert(key=key, minhash=minDict[key])
    #
    # print("\n")
    # print(f'LSH processing done time taken is {time.time() - t_initial} secs')
    # print("\n")
    #
    # print("Finding out similar items...")
    # create_candidate_pairs(dict(minDict))
    # print("\n")
    #
    # print("\n\n")
    # print(f"Total processing time is {time.time() - t_initial} secs")
