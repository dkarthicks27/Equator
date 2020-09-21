import os
from datasketch import MinHash
import time
import argparse
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

def operation(qry, size=5):
    # array = []
    # for y in range(0, len(qry) - size + 1):
    #     array.append(qry[y:y + size])
    array = qry.split()
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    return minhash, len(stream_set)


if __name__ == '__main__':
    # ap = argparse.ArgumentParser()
    #
    # # Add the arguments to the parser
    # ap.add_argument("-q", "--query", required=True, help="search query", metavar="", nargs='*')
    # args = vars(ap.parse_args())
    # buf = ''.join(args['query'])
    buf = '''
E-mail transmission cannot be guaranteed to be secure or error-free
as information could be intercepted, corrupted, lost, destroyed,
arrive late or incomplete, or contain viruses.  The sender therefore
does not accept liability for any errors or omissions in the contents
of this message which arise as a result of e-mail transmission.  If
verification is required please request a hard-copy version.  This
message is provided for informational purposes and should not be
construed as a solicitation or offer to buy or sell any securities or
related financial instruments.'''

    # this program uses minhash Ensemble for querying
    t1 = time.time()
    minhash_location = os.path.join(r'/Users/karthickdurai/Equator/LSH/containment/', 'hash_pickle.pc')

    lsh_ensemble_location = r'/Users/karthickdurai/Equator/LSH/containment/lsh_ensemble.pc'

    Dict = pickle.load(open(minhash_location, 'rb'))
    lshEnsemble = pickle.load(open(lsh_ensemble_location, 'rb'))

    mHash, size = operation(buf)
    similarItems = lshEnsemble.query(mHash, size)
    for i in similarItems:
        print(i, mHash.jaccard(MinHash(hashvalues=Dict[i])))

    print(f'time taken {time.time() - t1}')
