import os
from datasketch import MinHash
import time
import pyodbc
import sys
import pickle
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
    return minhash, len(stream_set)


def jaccard(a, b):
    if len(a) != len(b):
        raise ValueError("Cannot compute Jaccard given MinHash with\
                        different numbers of permutation functions")
    print(np.float(np.count_nonzero(a == b)))
    print(np.float(np.count_nonzero(a)))
    print('\n')
    return np.float(np.count_nonzero(a == b)) / np.float(len(a))


if __name__ == '__main__':
    # ap = argparse.ArgumentParser()
    #
    # # Add the arguments to the parser
    # ap.add_argument("-q", "--query", required=True, help="search query", metavar="", nargs='*')
    # args = vars(ap.parse_args())
    # buf = ''.join(args['query'])
    buf = '''From: Laurel Adams [/o=cw-test/ou=first administrative group/cn=recipients/cn=laurel.adams]
To: Sara Shackleton
Subject: TR Bond Swap Confirmation

Importance:     Normal
Priority:       Normal
Sensitivity:    None
'''

    # this program uses minhash Ensemble for querying
    t1 = time.time()
    minhash_location = os.path.join(r'/Users/karthickdurai/Equator/LSH/containment/', 'hash_pickle.pc')

    Dict = pickle.load(open(minhash_location, 'rb'))
    mHash, size = operation(buf)

    for i in Dict:
        print(i)
        jac = jaccard(mHash.hashvalues, Dict[i])
        if jac > 0.50:
            print(i, jac)

    print(f'time taken {time.time() - t1}')
