from pandas import DataFrame as df
from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
import time
import glob


def get_shingles(f1, size):
    buf = f1.read()  # read entire file
    array = []
    for y in range(0, len(buf) - size + 1):
        array.append(buf[y:y + size])
    return array


# Create minHash from document set and store it to the minDict dictionary
def hashLSH(stream_set, doc_id):
    minhash = MinHash(num_perm=NUM_PERMUTATION, seed=3)
    print(minhash, '\n')
    for d in stream_set:
        minhash.update(d.encode('utf8'))
    print(minhash.hashvalues)
    print(len(minhash.hashvalues))
    print(minhash.hashfunc)

    print('\n\n\n')
    minDict[doc_id] = minhash


def create_candidate_pairs():
    similarity = []
    for query in minDict.keys():
        bucket = lsh.query(minDict[query])
        print(bucket)

        if len(bucket) > 1:
            _a = bucket[0]
            for value in bucket[1:]:
                _b = value
                with open(_a, errors="ignore") as f1, open(_b, errors="ignore") as f2:
                    shingle1 = set(get_shingles(f1, 3))
                    shingle2 = set(get_shingles(f2, 3))
                    jaccard_similarity = len(shingle1.intersection(shingle2))/len(shingle1.union(shingle2))
                similarity.append((_a, _b, minDict[query].jaccard(minDict[_b]), jaccard_similarity))

        if len(similarity) == 1000:
            my_df = df(similarity, columns=['doc_id', 'duplicate_doc', 'minhash similarity', 'Jaccard Similarity'])
            with open('file.csv', 'a+') as csv_file:
                my_df.to_csv(path_or_buf=csv_file, index=False)
            similarity.clear()
            del my_df

    if len(similarity) > 0:
        my_df = df(similarity, columns=['doc_id', 'duplicate_doc', 'similarity_percent', 'Jaccard Similarity'])
        with open('file.csv', 'a+') as csv_file:
            my_df.to_csv(path_or_buf=csv_file, index=False)
        similarity.clear()
        del my_df


# this is the main function
# execution starts here
if __name__ == '__main__':
    t_initial = time.time()

    fileList = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    fileList = fileList[:10]

    # SET THE NO. OF PERMUTATIONS
    NUM_PERMUTATION = 256
    NUM_SHINGLES = 5  # THIS IS THE NUMBER OF SHINGLES THE DOC NEEDS TO DIVIDED INTO
    minDict = {}  # This is the dictionary containing all minhash key and value

    t0 = time.time()
    # pBar = tqdm(fileList)  # just an progress meter
    i = 0
    for file in tqdm(fileList, desc="Processing"):
        with open(file, errors="ignore") as f:
            x = set(get_shingles(f, NUM_SHINGLES))
            hashLSH(stream_set=x, doc_id=file)
            i += 1
            f.close()

    print("\n")
    print(f'Shingle creation done processing time: {time.time() - t0} secs')
    print("\n")


    t1 = time.time()


    lsh = MinHashLSH(threshold=0.80, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(minDict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=minDict[key])


    print(lsh.hashtables)
    print(len(lsh.hashtables))
    print(lsh.hashranges)
    print(lsh.h)
    print(f'lsh.b = {lsh.b}', '\n',  f"lsh.r = {lsh.r}", '\n', f"lsh.keys = {lsh.keys}", '\n', '\n', lsh.prepickle)
    print("\n\n")
    for i in lsh.get_counts():
        print(i)
    print(f'LSH processing done time taken is {time.time() - t1} secs')
    print("\n")

    print("Finding out similar items...")
    # sim = create_candidate_pairs()
    create_candidate_pairs()
    # print("\n")

    # pprint(sim)
    print("\n\n")
    print(f"Total processing time is {time.time() - t_initial} secs")

