from GensimApproach import corpora, models
from GensimApproach.utils import simple_preprocess
import glob
import os

from smart_open import smart_open

path = '/home/eqt2/OneDoc/*.txt'


class ReadTextFiles(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield simple_preprocess(line)


class BoWCorpus(object):
    def __init__(self, path, dictionary):
        self.filepath = path
        self.dictionary = dictionary

    def __iter__(self):
        # global mydict  # OPTIONAL, only if updating the source dictionary.
        for fname in os.listdir(self.filepath):
            for line in smart_open(os.path.join(self.filepath, fname), encoding='utf-8', decode_error='ignore'):
                # tokenize
                tokenized_list = simple_preprocess(line, deacc=True)

                # create bag of words
                bow = self.dictionary.doc2bow(tokenized_list, allow_update=True)

                # update the source dictionary (OPTIONAL)
                # mydict.merge_with(self.dictionary)

                # lazy return the BoW
                yield bow


file_path = r'/Users/karthickdurai/Equator/OneDoc/'
docs = glob.glob(path)
dic = corpora.Dictionary(ReadTextFiles(file_path))
bowCorpus = BoWCorpus(file_path, dic)

tfidf = models.TfidfModel(bowCorpus)
corpus_tfidf = tfidf[bowCorpus]
# for doc in tfidf[bowCorpus]:
# print([[dic[id], np.around(freq, decimals=2)] for id, freq in doc])



lda_model = models.LdaMulticore(corpus_tfidf, id2word=dic, num_topics=5, passes=2, workers=2)
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
