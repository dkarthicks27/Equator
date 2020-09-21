import os
from itertools import repeat
from datasketch import MinHash, MinHashLSHEnsemble
import time
import multiprocessing as mp
import pyodbc
import sys
import glob
import pickle
from tqdm import tqdm


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
    with open(file, errors="ignore") as f1:
        buf = f1.read()  # read entire file
    # array = []
    # for y in range(0, len(buf) - size + 1):
    #     array.append(buf[y:y + size])
    # print(array)
    array = buf.split()
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    d[file] = (minhash, len(stream_set))



if __name__ == '__main__':


    t1 = time.time()
    print("processing starts....")


    m = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    k = m


    Dict = mp.Manager().dict()
    NUM_PERMUTATION = 256

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    t_start = time.time()

    print("Starting minhash + shingle creation....")
    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)


    # Pickling the minhash by creating a pickle dictionary
    # this dictionary contains all the hashValues from the minhash
    # as we cannot actually pickle object stored at some memory location
    pickle_dict = {}
    for key in tqdm(Dict.keys(), desc="pickling the minhash...."):
        pickle_dict[key] = Dict[key][0].hashvalues

    minhash_location = os.path.join(r'/Users/karthickdurai/Equator/LSH/containment/', 'hash_pickle.pc')
    with open(minhash_location, 'wb') as f:
        pickle.dump(pickle_dict, f)

    del pickle_dict
    print(f"Completed creating and indexing minhash in {time.time() - t_start} secs\npickling the minhash.....")

    val = [(key, value[0], value[1]) for key, value in Dict.items()]
    lshEn = MinHashLSHEnsemble(threshold=0.50, num_perm=NUM_PERMUTATION, num_part=32)
    lshEn.index(val)
    location = r'/Users/karthickdurai/Equator/LSH/containment/lsh_ensemble.pc'
    with open(location, 'wb') as f:
        pickle.dump(lshEn, f)
    print(f'pickle file saved at: {location}')
