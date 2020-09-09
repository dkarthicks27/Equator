from datasketch import MinHash
import time

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
    array = []
    for y in range(0, len(qry) - size + 1):
        array.append(qry[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    return minhash, len(stream_set)



if __name__ == '__main__':

    # this program uses minhash Ensemble for querying
    t1 = time.time()

    pickle_file_directory = r'/LSH/pickle.pc'

    query = r'/Users/karthickdurai/Equator/OneDoc/hello.txt'


    lshEnsemble = pickle.load(open(pickle_file_directory, 'rb'))

    with open(query, errors="ignore") as q:
        buf = q.read()
        mHash, size = operation(buf)
    similarItems = lshEnsemble.query(mHash, size)
    for i in similarItems:
        print(i)

    print(f'time taken {time.time() - t1}')