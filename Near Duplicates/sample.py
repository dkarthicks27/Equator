from glob import glob
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pandas as pd


def preProcess(s):
    k = re.sub('[0-9]', '', s)
    return k


filePath = glob('/Users/karthickdurai/Equator/OneDoc/*.txt')
vectorizer = TfidfVectorizer(ngram_range=(2, 4), stop_words='english', input="filename", decode_error="ignore", preprocessor=preProcess)
vectorizer.fit_transform(filePath)
k = pd.DataFrame(vectorizer.get_feature_names())
print(k)