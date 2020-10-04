from gensim import corpora
from gensim import similarities
from glob import glob
from nltk.corpus import stopwords
from gensim.models import TfidfModel
from gensim import models

stop_words = stopwords.words('english')


class BoWCorpus(object):
    def __init__(self, path, dictionary):
        self.filepath = path
        self.dictionary = dictionary

    def __iter__(self):
        # global mydict  # OPTIONAL, only if updating the source dictionary.

        for file in self.filepath:
            with open(file, errors='ignore') as f:
                buf = f.read()

            buf = [word for word in buf.lower().split() if word not in stop_words]
            bow = self.dictionary.doc2bow(buf, allow_update=True)
            yield bow


# Create the Dictionary
mydict = corpora.Dictionary()

fileList = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
fileList = fileList[:50]
# Create the Corpus
bow_corpus = BoWCorpus(fileList, dictionary=mydict)  # memory friendly
# tfidf = TfidfModel(bow_corpus, dictionary=mydict, smartirs='ntc')
lsi_model = models.LsiModel(corpus=bow_corpus)
# lsi = lsi_model[tfidf[bow_corpus]]
# for i in lsi:
#     print(i)
# index = similarities.SparseMatrixSimilarity(corpus=tfidf[bow_corpus])

query = '''From: William Bradford [/o=cw-test/ou=first administrative group/cn=recipients/cn=william.bradford]
To: Paul Radous
CC: Sara Shackleton
Subject: Margin leverage and Enron Guarantee

Importance:     Normal
Priority:       Normal
Sensitivity:    None

Paul,

Can you work with Sara on this?

Bill

---------------------- Forwarded by William S Bradford/HOU/ECT on 07/28/2000 
07:31 PM ---------------------------
   
	
	
	From:  Sheila Glover                           07/28/2000 01:23 PM
	

To: William S Bradford/HOU/ECT@ECT, Sara Shackleton/HOU/ECT@ECT
cc: Jeff Kinneman/HOU/ECT@ECT, John Greene/HOU/ECT@ECT, Gary 
Hickerson/HOU/ECT@ECT 
Subject: Margin leverage and Enron Guarantee'''

index = similarities.Similarity(corpus=lsi_model[bow_corpus], num_features=lsi_model.num_topics, output_prefix='output')


query_doc = [word for word in query.lower().split() if word not in stop_words]
query_bow = mydict.doc2bow(query_doc, allow_update=True)


# query_lsi = lsi_model[query_bow]

sims = index[lsi_model[query_bow]]

sims = sorted(enumerate(sims), key=lambda item: -item[1])

for i, s in enumerate(sims):
    print(s, fileList[i])

# Print the token_id and count for each line.
# for line in bow_corpus:
#     print(line)
