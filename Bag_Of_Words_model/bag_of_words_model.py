class BagOfWords:
    import pandas as pd
    import numpy as np
    import nltk
    import re
    import matplotlib.pyplot as plt

    file1 = open(r'/home/eqt2/50K Text Docs/173.txt', 'r+')
    corpus = nltk.sent_tokenize(file1.read())
    for i in range(len(corpus)):
        corpus[i] = corpus[i].lower()
        corpus[i] = re.sub(r'\W', ' ', corpus[i])
        corpus[i] = re.sub(r'\s+', ' ', corpus[i])

    # print(corpus)
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

    # print(most_freq)
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

    sentence_vectors = np.asarray(sentence_vectors)
    # print(len(sentence_vectors))
    # print(sentence_vectors[831])
    names = list(wordFrequency.keys())
    values = list(wordFrequency.values())
    # print(sentence_vectors[100])
    df = pd.DataFrame(sentence_vectors, columns=most_freq)
    print(df)
    # EOF bag of words vector created
