import pickle
import numpy as np


def jaccard(a, b):
    if len(a) != len(b):
        raise ValueError("Cannot compute Jaccard given MinHash with\
                        different numbers of permutation functions")
    return np.float(np.count_nonzero(a == b)) / np.float(len(a))



location = r'/Users/karthickdurai/Equator/conceptual search/pickle.pc'
pickle_directory = pickle.load(open(location, 'rb'))


file_a = r'/Users/karthickdurai/Equator/OneDoc/117.txt'
file_b = r'/Users/karthickdurai/Equator/OneDoc/120.txt'


jac = jaccard(pickle_directory[file_a], pickle_directory[file_b])
print(jac)




