import glob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from sparse_dot_topn import awesome_cossim_topn
from sklearn.metrics.pairwise import cosine_similarity
import sys
import pyodbc


def sql_connect():
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=KARTHICK\SQLEXPRESS;"
            "Database=EQUATOR;"
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




def tfidf(filepath, n_gram=(1, 1)):
    print(f"Tfidf Started")
    Vectorizer = TfidfVectorizer(input='filename', use_idf=True,
                                 stop_words='english',
                                 decode_error='ignore', max_df=0.50, sublinear_tf=True, ngram_range=n_gram)
    vectors = Vectorizer.fit_transform(filepath)
    print(f'time taken to run tfidf is {time.time()-start_time} sec\n')
    return vectors


def normal_similarity():
    print("normal similarity\n")
    start = time.time()
    norm_a = np.linalg.norm(Vectors[1])
    norm_b = np.linalg.norm(Vectors[1])
    res = np.dot(Vectors[1], Vectors[1])/(norm_a * norm_b)
    print(res)




def cythonSimilarity():
    c1 = time.time()
    similarity = awesome_cossim_topn(Vectors, Vectors.transpose(), ntop=10, use_threads=True, n_jobs=4)
    c2 = time.time() - c1
    print(f"time taken for awesome_similarity is {c2} sec\n")


def similarity_normal():
    s1 = time.time()
    similar = cosine_similarity(Vectors, dense_output=False)
    s2 = time.time() - s1
    print(f"time taken for awesome_similarity is {s2} sec\n")



if __name__ == '__main__':
    start_time = time.time()
    #
    #
    # connect = sql_connect()
    # read_statement = input("enter the filePath retrieval statement: ")
    # tuple_filePath_doc_id = read_sql_input(connect, read_statement)
    #
    #
    # filePath = [filepath[1] for filepath in tuple_filePath_doc_id]
    filePath = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    Vectors = tfidf(filePath, n_gram=(1, 3))
    normal_similarity()

    # cythonSimilarity()
    # similarity_normal()
    print(Vectors[1])
    print(Vectors.shape)

    end_time = time.time() - start_time
    print(f'The Total time taken to complete is {end_time} sec')
