# so here we are going to test out how to build a custom preprocessor
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from glob import glob
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = set(stopwords.words('english'))


def preprocess(doc):
    sent = sent_tokenize(doc)
    words = []
    for line in sent:
        li = word_tokenize(line)
        words.append([selective for selective in li if selective not in stop_words])
    return words


file1 = [open("/Users/karthickdurai/Equator/OneDoc/120.txt").read()]
# filePath = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
tfidf = TfidfVectorizer(preprocessor=preprocess, input="content")

k = tfidf.fit_transform(file1)
print(k)
