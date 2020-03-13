#import pandas as pd
#from sklearn.feature_extraction.text import TfidfVectorizer
#from glob import glob
import timeit

#file_names = glob(r'/home/eqt2/OneDoc/*.txt')
#tfidf = TfidfVectorizer(input='filename', stop_words='english', encoding='utf-8', decode_error='ignore')
#vect = tfidf.fit_transform(file_names)

# print(vect)
# print(vect.toarray())
#listToStr = ['  '.join([str(elem) for elem in s]) for s in vect.toarray()]
#k = pd.DataFrame(listToStr)

#from sqlalchemy import create_engine

#mydb = create_engine("mysql+mysqlconnector://root:password@localhost/python")
#k.to_sql(name='newTable', con=mydb, if_exists='replace')
# print(k)
#down = pd.read_sql('SELECT * FROM newTable;', con=mydb)
#val = []
#for i in range(36):
#    val.append([float(i) for i in down.values[i][1].split()])

#print(pd.DataFrame(val))
code_to_test = """
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob

file_names = glob(r'/home/eqt2/50K Text Docs/*.txt')
tfidf = TfidfVectorizer(input='filename', stop_words='english', encoding='utf-8', decode_error='ignore')
vect = tfidf.fit_transform(file_names)

listToStr = ['  '.join([str(elem) for elem in s]) for s in vect.toarray()]
k = pd.DataFrame(listToStr)

from sqlalchemy import create_engine

mydb = create_engine("mysql+mysqlconnector://root:password@localhost/python")
down = pd.read_sql('SELECT * FROM newTable', con=mydb)
# val = list(map(float, down.values[3][1].split()))
#val = [float(i) for i in down.values[3][1].split()]
val = []
for i in range(36):
    val.append([float(i) for i in down.values[i][1].split()])

#print(pd.DataFrame(val))
"""

elapsed_time = timeit.timeit(stmt=code_to_test, number=1)
print(elapsed_time)
