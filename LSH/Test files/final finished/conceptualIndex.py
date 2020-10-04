import argparse
import pickle
import os
import sys
from itertools import repeat
import pyodbc
from nltk.corpus import stopwords
import multiprocessing as mp
import time
import hashlib

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

def operation(index, inp):
    doc_id = inp[0]
    filepath = inp[1]
    with open(filepath, errors='ignore') as f:
        buf = f.read()
    array = [word for word in buf.lower().split() if word not in stopWords]
    stream_set = set(array)
    final = set()
    for word in stream_set:
        m = hashlib.sha256()
        m.update(word.encode('utf-8'))
        final.add(m.hexdigest())
    index[doc_id] = final




if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-s", "--server", required=True, help="server name", metavar="")
    ap.add_argument("-d", "--database", required=True, help="database name", metavar="")
    ap.add_argument("-q", "--query", required=True, help="Sql query", metavar="")
    ap.add_argument("-o", "--output", required=True, help="Pickle output directory", metavar="")
    args = vars(ap.parse_args())
    filePath = args['output']


    t1 = time.time()
    print('processing starts..../n')



    # connecting to sql is done by following the below code
    connect = sql_connect(args['server'], args['database'])
    k = read_sql_input(connect, args['query'])
    k = [element for element in k if os.path.isfile(element[1]) and element[1].endswith('.txt')]




    # creating and pickling stopwords
    if os.path.isfile(os.path.join(filePath, 'stopwords.pc')):
        print('Using the stopwords pickle file')
        stopWords = pickle.load(open(os.path.join(filePath, 'stopwords.pc'), 'rb'))
    else:
        print('there is no local stopwords available importing from NLTK....')
        stopWords = set(stopwords.words('english'))
        with open(os.path.join(filePath, 'stopwords.pc'), 'wb') as s:
            pickle.dump(stopWords, s)





    # Manger dictionary is created which is used as a shared resource
    Dict = mp.Manager().dict()

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    t_start = time.time()

    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)



    print('index creation done.../n creating pickle....')
    with open(os.path.join(filePath, 'index.pc'), mode='wb') as pc:
        pickle.dump(dict(Dict), pc)

    print(f'Time taken is {time.time() - t_start}')
