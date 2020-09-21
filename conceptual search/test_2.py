import pickle
from datasketch import MinHash
import numpy as np

def operation(qry, size=5):
    array = []
    for y in range(0, len(qry) - size + 1):
        array.append(qry[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    return minhash


def jaccard(a, b):
    if len(a) != len(b):
        raise ValueError("Cannot compute Jaccard given MinHash with\
                        different numbers of permutation functions")
    return np.float(np.count_nonzero(a == b)) / np.float(len(a))


f = pickle.load(open('pickle_dict.pc', 'rb'))
query = '''From: Laurel Adams [/o=cw-test/ou=first administrative group/cn=recipients/cn=laurel.adams]
To: Sara Shackleton
Subject: TR Bond Swap Confirmation

Importance:     Normal
Priority:       Normal
Sensitivity:    None

Sara,'''



mHash = operation(query)

result = []
for key in f.keys():
    jc = jaccard(mHash, f[key])
    if jc > 0.40:
        result.append((key, jc))

print(result)
