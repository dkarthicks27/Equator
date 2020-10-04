import hashlib
import pickle
import os


def jaccard(a, b):

    return len(a.intersection(b))/len(a)



def findHash(string):
    stream_set = set(string)
    final = set()
    for word in stream_set:
        m = hashlib.sha256()
        m.update(word.encode('utf-8'))
        final.add(m.hexdigest())
    return final


if __name__ == '__main__':
    # Loading both index dictionary and the stopwords
    with open('index.pc', 'rb') as f:
        Dict = pickle.load(f)
    stopWords = pickle.load(open('stopwords.pc', 'rb'))


    qry = '''ENA Public Relations'''
    threshold = 0.90
    # preparing the query
    # cleaning the query and hashing the query
    buf = [word for word in qry.lower().split() if word not in stopWords]
    query = findHash(buf)


    # performing query to see matching documents
    for i in Dict:
        sims = jaccard(query, Dict[i])
        if sims >= threshold:
            print(f'query is {sims*100} percent similar {os.path.basename(i)}')
