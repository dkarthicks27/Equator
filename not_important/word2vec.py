from GensimApproach.models import Word2Vec
import nltk
from nltk.cluster import KMeansClusterer
import re
import numpy as np
from GensimApproach.models import word2vec

file1 = open(r'/home/eqt2/50K Text Docs/3410.txt', 'r+')
corpus = nltk.sent_tokenize(file1.read())
for i in range(len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub(r'\W', ' ', corpus[i])
    corpus[i] = re.sub(r'\s+', ' ', corpus[i])
sentences = []
for sentence in corpus:
    tokens = nltk.word_tokenize(sentence)
    sentences.append(tokens)
# print(sentences)
# sentences = np.asarray(sentences)
models = Word2Vec(sentences, min_count=1)
X = models.wv[models.wv.vocab]
NUM_CLUSTERS = 3
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
# print(assigned_clusters)
words = list(models.wv.vocab)
cluster0 = []
cluster1 = []
cluster2 = []
for i, word in enumerate(words):
    nltk.pprint(word + ":" + str(assigned_clusters[i]))
