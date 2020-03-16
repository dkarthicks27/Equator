import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import mysql.connector

file_names = glob(r'/home/eqt2/10 Documents/*.txt')
tfidf = TfidfVectorizer(input='filename', stop_words='english', encoding='utf-8', decode_error='ignore',max_features=1000)
vect = tfidf.fit_transform(file_names)


# print(vect)
# print(vect.toarray())
#def convert_to_string(vector):
    #listToStr = ' '.join([str(elem) for elem in vector])
    #df = pd.DataFrame(listToStr)
    # mydb1 = create_engine("mysql+mysqlconnector://root:password@localhost/python")
    #df.to_sql(name='newTable1', con=mydb, if_exists='append')


# for i in vect.toarray():
    # convert_to_string(i)

listToStr = ['  '.join([str(elem) for elem in s]) for s in vect.toarray()]
k = pd.DataFrame(listToStr)

from sqlalchemy import create_engine

mydb = create_engine("mysql+mysqlconnector://root:password@localhost/python")
k.to_sql(name='newTable', con=mydb, if_exists='replace')
# print(k)
#down = pd.read_sql('SELECT * FROM newTable;', con=mydb)
#val = []
#for i in range(36):
    #val.append([float(i) for i in down.values[i][1].split()])

#print(pd.DataFrame(val))

#for i in vect:
    # print(i.toarray())
    # convert_to_string(i.toarray())