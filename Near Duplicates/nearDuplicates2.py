# import hashlib
from glob import glob
import os
from GensimApproach import corpora
from nltk.corpus import stopwords
from GensimApproach.models import TfidfModel
import numpy as np
from GensimApproach.similarities import Similarity

filenames = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
path = r'/Users/karthickdurai/Equator/OneDoc/'
# def calculate_checksum(filenames):
# hash = hashlib.md5()
# hash.update(open(filenames, "rb").read())
# return hash.digest()


# x = []
# for fn in filenames:
# x.append(calculate_checksum(fn))

# print(x)

from GensimApproach.utils import simple_preprocess
from smart_open import smart_open

stop_words = stopwords.words('english')


class BoWCorpus(object):
    def __init__(self, path, dictionary):
        self.filepath = path
        self.dictionary = dictionary

    def __iter__(self):
        # global mydict  # OPTIONAL, only if updating the source dictionary.
        for file in self.filepath:
            for line in open(file, errors='ignore'):
                # tokenize
                tokenized_list = simple_preprocess(line, deacc=True)

                # create bag of words
                bow = self.dictionary.doc2bow(tokenized_list, allow_update=True)

                # update the source dictionary (OPTIONAL)
                # mydict.merge_with(self.dictionary)

                # lazy return the BoW
                yield bow


# Create the Dictionary
mydict = corpora.Dictionary()

# Create the Corpus
bow_corpus = BoWCorpus(path=filenames, dictionary=mydict)  # memory friendly
# tfidf = TfidfModel(corpus=bow_corpus, smartirs='ntc')
# for doc in tfidf[bow_corpus]:
    # print([[mydict[id], np.around(freq, decimals=2)] for id, freq in doc])


class ReadTxtFiles(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding='latin'):
                yield simple_preprocess(line)


dictionary = corpora.Dictionary(ReadTxtFiles(path))
# print(dictionary)
# for line in bow_corpus:
# print(line)

index = Similarity(corpus=bow_corpus, num_features=len(dictionary), output_prefix='out')
doc_id = 0
similar_docs = {}
for similarities in index:
    similar_docs[doc_id] = list(enumerate(similarities))
    doc_id += 1

print(similar_docs)
