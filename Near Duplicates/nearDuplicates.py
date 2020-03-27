from sklearn.model_selection import train_test_split
from snapy import MinHash, LSH
from glob import glob
import pandas as pd
import os


def readFiles():
    files = []
    path = '/Users/karthickdurai/Equator/OneDoc/'
    pathname = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    for fileName in pathname:
        with open(fileName, errors='ignore') as f:
            files.append(f.read())
            f.close()
    labels = os.listdir(path)
    return files, labels


def minhashing(files, labels):
    file, x, label, y = train_test_split(files, labels, train_size=0.10)
    minhash = MinHash(file, permutations=100, hash_bits=64, seed=3, n_gram=9)
    lsh = LSH(minhash, label, no_of_bands=50)
    print(lsh.edge_list(min_jaccard=0.5, jaccard_weighted=True))


if __name__ == '__main__':
    files, labels = readFiles()
    minhashing(files, labels)
