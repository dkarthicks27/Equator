import argparse
from itertools import repeat
from datasketch import MinHash, MinHashLSH
import time
import os
import multiprocessing as mp
import pyodbc
import sys
import pickle


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




if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-f", "--filepath", required=True, help="pickled directory file path", metavar="")
    ap.add_argument("-q", "--query", required=True, help="conceptual search query as string", metavar="")
    ap.add_argument("-t", "--threshold", required=True, help="threshold for conceptual search", metavar="")
    args = vars(ap.parse_args())

    # making variables of the arguments from the argument parser
    threshold = args['threshold']
    query = args['query']
    directory = args['filepath']
    k = os.path.join(directory, 'pickle.pc')
    print(k)

    NUM_PERMUTATION = 256  # parameter 1 which is the number of permutation
    minDict = pickle.load(open(os.path.join(directory, 'pickle.pc'), 'rb'))
    print(minDict)

    # lsh = MinHashLSH(threshold=0.90, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    # with lsh.insertion_session() as session:
    #     for key in tqdm(Dict.keys(), desc="LSH processing"):
    #         session.insert(key=key, minhash=Dict[key])
    t1 = time.time()
    print("processing starts....")
