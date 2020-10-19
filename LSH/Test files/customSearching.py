import hashlib
import pickle
import os
import time

def jaccard(a, b):

    return len(a.intersection(b))/len(a)



def findHash(string, shingle_range=(3, 5)):
    array = []
    stream_set = set()

    for i in string.lower().split():
        if i not in stream_set and i not in stopWords:
            stream_set.add(i)
            array.append(i)

    final = set()
    for word in stream_set:
        m = hashlib.sha256()
        m.update(word.encode('utf-8'))
        final.add(m.hexdigest())
    lowerRange = shingle_range[0]
    upperRange = shingle_range[1]

    if len(string) > lowerRange:
        for shingleLength in range(lowerRange, upperRange+1):
            for i in range(len(array) - shingleLength + 1):
                m = hashlib.sha256()
                word = ' '.join(array[i:i + shingleLength])
                m.update(word.encode('utf-8'))
                final.add(m.hexdigest())

    return final


if __name__ == '__main__':
    # Loading both index dictionary and the stopwords
    t1 = time.time()
    with open('index.pc', 'rb') as f:
        Dict = pickle.load(f)
    stopWords = pickle.load(open('stopwords.pc', 'rb'))


    qry = """Risk Assessment Unit"""
    threshold = 0.70
    # preparing the query
    # cleaning the query and hashing the query
    # buf = [word for word in qry.lower().split() if word not in stopWords]
    query = findHash(qry)


    # performing query to see matching documents
    for i in Dict:
        sims = jaccard(query, Dict[i])
        if sims >= threshold:
            pass
            print(f'query is {sims*100} percent similar {os.path.basename(i)}')
    print(f'time taken is {time.time() - t1}')