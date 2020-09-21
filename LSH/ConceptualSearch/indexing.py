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




if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-s", "--server", required=True, help="server name", metavar="")
    ap.add_argument("-d", "--database", required=True, help="database name", metavar="")
    ap.add_argument("-q", "--query", required=True, help="Sql query", metavar="")
    ap.add_argument("-o", "--output", required=True, help="Pickle output directory", metavar="")
    args = vars(ap.parse_args())

    t1 = time.time()
    print("processing starts....")

    # connecting to sql is done by following the below code
    connect = sql_connect(args['server'], args['database'])
    k = read_sql_input(connect, args['query'])
    k = [element for element in k if os.path.isfile(element[1]) and element[1].endswith('.txt')]


    # So a manager dictionary is created which is a shared resource in our case
    Dict = mp.Manager().dict()
    NUM_PERMUTATION = 256

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    t_start = time.time()

    print("Starting minhash + shingle creation....")
    # Let's start with the actual process of creating minhash and shingles
    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)

    # Pickling the minhash by creating a pickle dictionary
    # this dictionary contains all the hashValues from the minhash
    # as we cannot actually pickle object stored at some memory location
    pickle_dict = {}
    for key in tqdm(Dict.keys(), desc="pickling the minhash...."):
        pickle_dict[key] = Dict[key].hashvalues

    minhash_location = os.path.join(args['output'], 'hash_pickle.pc')
    with open(minhash_location, 'wb') as f:
        pickle.dump(pickle_dict, f)

    del pickle_dict
    print(f"Completed creating and indexing minhash in {time.time() - t_start} secs")
    # the process of minhash and its pickle is completely done

    # lsh is now initiated, we create a pickle file for it in the given directory
    # let's start the process
    lsh_location = os.path.join(args['output'], 'lsh_pickle.pc')

    lsh = MinHashLSH(threshold=0.50, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(Dict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=Dict[key])

    with open(lsh_location, 'wb') as f:
        pickle.dump(lsh, f)

    # so created and dumped the lsh file too

    print(f'pickle file saved at: {lsh_location}')
