import pickle
from datasketch import MinHash


def operation(file):
    size = 5
    with open(file, errors="ignore") as f1:
        buf = f1.read()  # read entire file
    array = []
    for y in range(0, len(buf) - size + 1):
        array.append(buf[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    return minhash


location = r'/Users/karthickdurai/Equator/conceptual search/pickle.pc'

with open(location, 'rb') as f:
    lsh = pickle.load(f)

mHash = operation(r'/Users/karthickdurai/Equator/OneDoc/117.txt')


print(lsh.query(mHash))
