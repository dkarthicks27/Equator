# GensimApproach is a library for data science similar to scikit and here we are going to use it very similar.
# first work given by anna was to find out classification using GensimApproach. For which
# the ideal class was to use the naive bayes or the logistic regression or the svc or Multinomial NB depends on
# our choice
from glob import glob
from gensim import corpora
import gensim

path = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')


class CountVectorizer(object):
    def __init__(self, path1, dictionary1):
        self.path = path1
        self.dictionary = dictionary1

    def __iter__(self):
        for file in self.path:
            for line in open(file):
                yield self.dictionary.doc2bow(line.lower().split())


class MyDict(object):
    def __iter__(self):
        for file in path:
            for line in open(file):
                yield corpora.Dictionary(line.lower().split())


text = r'/Users/karthickdurai/Equator/OneDoc/40.txt'
dictionary = (line.lower().split() for line in open(text))
for x in dictionary:
    print(x)


# for x in dictionary:
# print(x)


class Doc:
    def __iter__(self):
        for line in open(text):
            doc = line.lower().split()
            yield doc


eg = Doc()
for x in eg:
    print(x)