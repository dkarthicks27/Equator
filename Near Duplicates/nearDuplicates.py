from sklearn.model_selection import train_test_split
from snapy import MinHash, LSH
from glob import glob
import pandas as pd
import os


def readFiles():
    minh = MinHash("this is a dummy file", permutations=100, hash_bits=64, seed=3, n_gram=9)
    ls = LSH(minh, '0', no_of_bands=50)
    pathname = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    for fileName in pathname:
        files = []
        with open(fileName, errors='ignore') as f:
            files.append(f.read())
            if len(files) != 0:
                minhashing(files, fileName, ls)
            if pathname.index(fileName) == len(pathname) - 1:
                minhashing(files, fileName, ls, command=0)


def minhashing(file, label, lshalgo, command=-1, entry):
    minhash = MinHash(file, permutations=100, hash_bits=64, seed=3, n_gram=9)
    if entry == 0:
        lsh = LSH(minhash, label, no_of_bands=50)
    else:
        lsh.update()
    lsh = lshalgo
    lsh.update(minhash, label)
    if command == 0:
        print(lsh.edge_list(min_jaccard=0.5, jaccard_weighted=True))
    # file, x, label, y = train_test_split(files, labels, train_size=0.10)
    # lsh = LSH(minhash, label, no_of_bands=50)
    # print(lsh.edge_list(min_jaccard=0.5, jaccard_weighted=True))


if __name__ == '__main__':
    readFiles()
    # minhash = MinHash("this is a dummy file", permutations=100, hash_bits=64, seed=3, n_gram=9)
    # lsh = LSH(minhash, '0', no_of_bands=50)
