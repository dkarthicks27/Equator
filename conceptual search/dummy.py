import sys
from datetime import datetime

import pyodbc

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

import gensim
from gensim import models
from gensim import corpora
from gensim.similarities import Similarity
from gensim.utils import simple_preprocess
from smart_open import smart_open
import os
from glob import glob


def sql_connect(server="KARTHICK\SQLEXPRESS", database="EQUATOR"):
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


# this class will help us make bag of words corpus object
class BoWCorpus(object):
    def __init__(self, path, dictionary):
        self.filepath = path
        # self.files = glob(path + '*.txt')
        self.dictionary = dictionary

    def __iter__(self):
        # global mydict  # OPTIONAL, only if updating the source dictionary.
        for file in self.filepath:
            for line in open(file, errors="ignore"):
                # tokenize
                tokenized_list = simple_preprocess(line, deacc=True)

                # create bag of words
                bow = self.dictionary.doc2bow(tokenized_list, allow_update=True)

                # update the source dictionary (OPTIONAL)
                # mydict.merge_with(self.dictionary)

                # lazy return the BoW
                yield bow



if __name__ == '__main__':
    sql = input("Enter the sql insert statement: ")
    connection = sql_connect()
    k = read_sql_input(connection, sql)
    # Create the Dictionary
    mydict = corpora.Dictionary()
    print("\ndictionary formation done\n")
    # Create the Corpus
    filePath = [seq[1] for seq in k]
    bow_corpus = BoWCorpus(path=filePath, dictionary=mydict)  # memory friendly
    print("bow corpus done\n")

    # form tfidf using this
    tfidf = models.TfidfModel(bow_corpus, smartirs='ntc')
    print("tfidf formation done")
    index = Similarity(corpus=tfidf[bow_corpus],
                       num_features=len(mydict),
                       output_prefix='on_disk_output')
    this = datetime.now()

    later_time = this.strftime("%H:%M:%S")
    print("Current Time =", later_time)

    print("The time elapsed is {}".format(this - now))
