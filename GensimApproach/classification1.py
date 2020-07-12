import gensim
from gensim import models
from gensim import corpora
from gensim.similarities import Similarity
from gensim.utils import simple_preprocess
from smart_open import smart_open
import os
from glob import glob


class BoWCorpus(object):
    def __init__(self, path, dictionary):
        self.filepath = path
        self.files = glob(path + '*.txt')
        self.dictionary = dictionary

    def __iter__(self):
        # global mydict  # OPTIONAL, only if updating the source dictionary.
        for file in self.files:
            for line in open(file, errors="ignore"):
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
print("dictionary formation done\n")
# Create the Corpus
bow_corpus = BoWCorpus(path='/Users/karthickdurai/Equator/OneDoc/', dictionary=mydict)  # memory friendly
print("bow corpus done\n")
# dictionary = corpora.Dictionary(ReadTxtFiles(path_to_text_directory))
# print(bow_corpus)

# mydict.save('mydict.dict')  # save dict to disk
# corpora.MmCorpus.serialize('bow_corpus.mm', bow_corpus)

tfidf = models.TfidfModel(bow_corpus, smartirs='ntc')
print("tfidf formation done")
index = Similarity(corpus=tfidf[bow_corpus],
                   num_features=len(mydict),
                   output_prefix='on_disk_output')
print("similarity done")
