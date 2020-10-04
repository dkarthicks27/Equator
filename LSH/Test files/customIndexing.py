import pickle
import os
from itertools import repeat
from nltk.corpus import stopwords
from glob import glob
import multiprocessing as mp
import time
import hashlib


def operation(index, file):
    with open(file, errors='ignore') as f:
        buf = f.read()
    array = [word for word in buf.lower().split() if word not in stopWords]
    stream_set = set(array)
    final = set()
    for word in stream_set:
        m = hashlib.sha256()
        m.update(word.encode('utf-8'))
        final.add(m.hexdigest())
    index[file] = final




if __name__ == '__main__':
    t1 = time.time()
    fileName = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')

    k = fileName
    if os.path.isfile('stopwords.pc'):
        print('Using the stopwords pickle file')
        stopWords = pickle.load(open('stopwords.pc', 'rb'))
    else:
        print('there is no local stopwords available importing....')
        stopWords = set(stopwords.words('english'))
        with open('stopwords.pc', 'wb') as s:
            pickle.dump(stopWords, s)


    Dict = mp.Manager().dict()

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    t_start = time.time()

    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)


    with open('index.pc', mode='wb') as pc:
        pickle.dump(dict(Dict), pc)

    print(f'Time taken is {time.time() - t_start}')
