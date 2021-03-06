import argparse
from itertools import repeat
from datasketch import MinHash, MinHashLSH
import time
import os
import multiprocessing as mp
import pyodbc
import sys
import glob
import pickle


########################################################################################################################
# this section includes all the basic sql functions
from tqdm import tqdm


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



if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-o", "--output", required=True, help="Pickle output directory", metavar="")
    args = vars(ap.parse_args())


    t1 = time.time()
    print("processing starts....")


    k = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')


    Dict = mp.Manager().dict()
    NUM_PERMUTATION = 256

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    t_start = time.time()

    print("Starting minhash + shingle creation....")
    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)


    print(f"Completed creating and indexing minhash in {time.time() - t_start} secs\npickling the minhash.....")
    location = os.path.join(args['output'], 'pickle.pc')


    lsh = MinHashLSH(threshold=0.50, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(Dict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=Dict[key])

    with open(location, 'wb') as f:
        pickle.dump(lsh, f)
    print(f'pickle file saved at: {location}')
