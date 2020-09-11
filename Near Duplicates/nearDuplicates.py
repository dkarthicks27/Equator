import argparse
from itertools import repeat
from datasketch import MinHash, MinHashLSH
import time
import os
import multiprocessing as mp
from pandas import DataFrame as df
from tqdm import tqdm
import pyodbc
import sys


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


def operation(d, file, size=5):
    with open(file[1], errors="ignore") as f1:
        buf = f1.read()  # read entire file
    array = []
    for y in range(0, len(buf) - size + 1):
        array.append(buf[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    d[file[0]] = minhash


def create_candidate_pairs(queryDict):
    similarity = []
    for query in queryDict.keys():
        bucket = lsh.query(queryDict[query])

        if len(bucket) > 1:
            _a = bucket[0]
            for value in bucket[1:]:
                _b = value
                similarity.append((_a, _b, queryDict[query].jaccard(queryDict[_b])))

        if len(similarity) == 1000:
            my_df = df(similarity, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
            with open('file.csv', 'a+') as csv_file:
                my_df.to_csv(path_or_buf=csv_file, index=False)
            similarity.clear()
            del my_df


    if len(similarity) > 0:
        my_df = df(similarity, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
        with open('file.csv', 'a+') as csv_file:
            my_df.to_csv(path_or_buf=csv_file, index=False)
        similarity.clear()
        del my_df


if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-s", "--server", required=True,
                    help="server name")
    ap.add_argument("-d", "--database", required=True,
                    help="database name")
    ap.add_argument("-q", "--query", required=True,
                    help="Sql query")
    args = vars(ap.parse_args())

    t1 = time.time()
    print("processing starts....")

    # THIS IS THE SQL CONNECTION AND QUERYING STATEMENT:
    # sql = input("Enter the sql insert statement: ")
    connect = sql_connect(args['server'], args['database'])
    k = read_sql_input(connect, args['query'])
    path = [element for element in k if os.path.isfile(element[1]) and element[1].endswith('.txt')]


    Dict = mp.Manager().dict()
    NUM_PERMUTATION = 256

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    print("Starting minhash + shingle creation....")
    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)


    print("Completed creating minhash\nCreating LSH......")
    t2 = time.time()

    lsh = MinHashLSH(threshold=0.90, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(Dict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=Dict[key])


    print(f"{time.time() - t2} secs was taken to create LSH")

    print("\nfinding candidate pairs.....")
    create_candidate_pairs(dict(Dict))


    print("\ncandidate pairs done")
    print(f"total time : {time.time() - t1} secs")



