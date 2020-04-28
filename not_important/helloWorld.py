import os
from glob import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
from sklearn.model_selection import train_test_split

pathFile = '/Users/karthickdurai/Equator/OneDoc/300.txt'
path = glob(pathname='/Users/karthickdurai/Equator/OneDoc/*.txt')
#path, pathy = train_test_split(path, train_size=0.05, shuffle=True)
tfidf = TfidfVectorizer(input="filename", decode_error="ignore")
x = tfidf.fit_transform(path)
# TfidfVectorizer()
print(tfidf.get_feature_names())
tfidf.input = "content"
# print(tfidf.input)
inp = ["From: Outlook Migration Team [outlook migration team]"
       "Subject: Joe Sutton re: Azurix"
       "Importance:     Normal"
       "Priority:       Normal"
       "Sensitivity:    None"]
vec = tfidf.transform(inp)
similarity = cosine_similarity(vec, x)
print(similarity)
