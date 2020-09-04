from itertools import repeat
from datasketch import MinHash, MinHashLSH
from glob import glob
import time
import multiprocessing as mp
from pandas import DataFrame as df
from tqdm import tqdm


def operation(d, f):
    with open(f, errors="ignore") as f1:
        buf = f1.read()  # read entire file
    array = []
    for y in range(0, len(buf) - size + 1):
        array.append(buf[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=NUM_PERMUTATION)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    try:
        d[f] = minhash
    finally:
        pass




def create_candidate_pairs(minDict):
    similarity = []
    for query in minDict.keys():
        bucket = lsh.query(minDict[query])

        if len(bucket) > 1:
            _a = bucket[0]
            for value in bucket[1:]:
                _b = value
                similarity.append((_a, _b, minDict[query].jaccard(minDict[_b])))

        if len(similarity) == 1000:
            my_df = df(similarity, columns=['doc_id', 'duplicate_doc', 'minhash similarity'])
            with open('file.csv', 'a+') as csv_file:
                my_df.to_csv(path_or_buf=csv_file, index=False)
            similarity.clear()
            del my_df

    if len(similarity) > 0:
        my_df = df(similarity, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
        with open('file.csv', 'a+') as csv_file:
            my_df.to_csv(path_or_buf=csv_file, index=False)
        similarity.clear()
        del my_df



if __name__ == '__main__':
    t1 = time.time()
    print("processing starts....")

    filePath = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    Dict = mp.Manager().dict()
    NUM_PERMUTATION = 256
    size = 3


    iterable = zip(repeat(Dict, len(filePath)), filePath)
    print(f'{time.time() - t1} secs taken to initiate')
    with mp.Pool() as pool:
        pool.starmap(operation, iterable)


    print("Completed creating minhash\nCreating LSH......")

    lsh = MinHashLSH(threshold=0.90, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(Dict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=Dict[key])


    print(f"total time : {time.time() - t1} secs")

    print("\nfinding candidate pairs.....")
    create_candidate_pairs(Dict)


    print("\ncandidate pairs done")
    print(f"total time : {time.time() - t1} secs")