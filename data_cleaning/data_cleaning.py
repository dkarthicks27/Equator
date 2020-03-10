import pandas as pd
import numpy as np
import nltk
import re
from pprint import pprint
from nltk.corpus import stopwords

file1 = open(r'/home/eqt2/50K Text Docs/173.txt', 'r+')
corpus = nltk.sent_tokenize(file1.read())
for i in range(len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub(r'\W', ' ', corpus[i])
    corpus[i] = re.sub(r'\s+', ' ', corpus[i])

# print(corpus[105])
wordFrequency = {}
for eachSentence in corpus:
    tokens = nltk.word_tokenize(eachSentence)
    for token in tokens:
        if token not in wordFrequency.keys():
            wordFrequency[token] = 1
        else:
            wordFrequency[token] += 1

# print(wordFrequency)
import heapq

most_freq = heapq.nlargest(200, wordFrequency, key=wordFrequency.get)

# print(most_freq[0])
sentence_vectors = []
for sentence in corpus:
    sentence_tokens = nltk.word_tokenize(sentence)
    sent_vec = []
    for token in most_freq:
        if token in sentence_tokens:
            sent_vec.append(1)
        else:
            sent_vec.append(0)
    sentence_vectors.append(sent_vec)

sentence_vectors = pd.DataFrame(np.asarray(sentence_vectors))
# print(sentence_vectors)

stopWords = set(stopwords.words('english'))
# print (stopWords)
file2 = open(r'/home/eqt2/50K Text Docs/418.txt', 'r+')
corp_word = nltk.word_tokenize(file2.read())
print(len(corp_word))

for i in range(len(corp_word)):
    corp_word[i] = corp_word[i].lower()
    corp_word[i] = re.sub(r'\W', ' ', corp_word[i])
    corp_word[i] = re.sub(r'\s+', ' ', corp_word[i])

filteredWords = []
for word in corp_word:
    if word not in stopWords:
        filteredWords.append(word)

print(filteredWords)
