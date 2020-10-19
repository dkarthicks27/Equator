import argparse
import pickle
import sys
import pyodbc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import os
import time


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

def tfidf(filePath, storage, n_gram=(1, 3)):
    print('Tfidf initiated\n')
    t_initial = time.time()
    vectorizer = TfidfVectorizer(input='filename', use_idf=True,
                                 stop_words='english',
                                 decode_error='ignore', max_df=0.50, sublinear_tf=True, ngram_range=n_gram,
                                 lowercase=True)
    vectors = vectorizer.fit_transform(filePath)
    print(f'Time taken to index the documents is {time.time() - t_initial}')
    # serializing the tfidf vectorizer to be used during the search operation where the query is first converted to
    # tfidf vector then the dimension reductionality is done using LSI
    vectorizer.input = 'content'
    with open(os.path.join(storage, 'tfidfVectorizer.pc'), 'wb') as vec:
        pickle.dump(vectorizer, vec)
    return vectors


def lsi(vectors, storage):
    t_initial = time.time()
    print('Performing Dimensionality reduction using LSI....\n')

    svd = TruncatedSVD(n_components=100)
    truncatedVectors = svd.fit_transform(vectors)
    # serializing the LSA applied vectors to use during cosine similarity performing
    with open(os.path.join(storage, 'vector.pc'), 'wb') as vec:
        pickle.dump(truncatedVectors, vec)
    # serialising the LSI model so that we can convert the query later
    with open(os.path.join(storage, 'svd.pc'), 'wb') as vectorizer:
        pickle.dump(svd, vectorizer)
    print(f'Completed LSI time taken is {time.time() - t_initial} secs')


######################################################################################################

if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-s", "--server", required=True, help="server name", metavar="")
    ap.add_argument("-d", "--database", required=True, help="database name", metavar="")
    ap.add_argument("-q", "--query", required=True, help="Sql query", metavar="")
    ap.add_argument("-o", "--output", required=True, help="Pickle output directory", metavar="")
    args = vars(ap.parse_args())
    output_directory = args['output']

    t1 = time.time()
    print('processing starts....\n')

    # connecting to sql is done by following the below code
    connect = sql_connect(args['server'], args['database'])
    k = read_sql_input(connect, args['query'])
    k = [element for element in k if os.path.isfile(element[1]) and element[1].endswith('.txt')]

    # once we have the doc_id, filepath array, we are going to serialise it as we need to use it for search query later
    # pickling the document id to filepath array so that we can use it while we perform search query
    doc_id = [x[0] for x in k]
    with open(os.path.join(output_directory, 'doc_id.pc'), 'wb') as s:
        pickle.dump(doc_id, s)

    vector = tfidf(filePath=[x[1] for x in k], storage=output_directory)
    lsi(vector, storage=output_directory)
