from itertools import repeat
from datasketch import MinHash, MinHashLSH
import time
import os
import multiprocessing as mp
import pickle
from tqdm import tqdm
from glob import glob


#####################################################################################################


def operation(d, file, size=5):
    with open(file, errors="ignore") as f1:
        buf = f1.read()  # read entire file
    array = []
    for y in range(0, len(buf) - size + 1):
        array.append(buf[y:y + size])
    stream_set = set(array)
    minhash = MinHash(num_perm=256)
    for x in stream_set:
        minhash.update(x.encode('utf8'))
    d[file] = minhash




if __name__ == '__main__':
    # Construct the argument parser
    query = '''From: Laurel Adams [/o=cw-test/ou=first administrative group/cn=recipients/cn=laurel.adams]
To: Sara Shackleton
Subject: TR Bond Swap Confirmation

Importance:     Normal
Priority:       Normal
Sensitivity:    None

Sara,

Paul wants to know if we have any objections to the attached form of 
confirmation.  Please let me know if you have any concerns.  Thank you!  
---------------------- Forwarded by Laurel Adams/HOU/ECT on 07/31/2000 05:00 
PM ---------------------------'''

    t1 = time.time()
    print("processing starts....")
    print(len(query))

    k = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    args = {'output': r'/Users/karthickdurai/Equator/LSH/ConceptualSearch/test'}
    # So a manager dictionary is created which is a shared resource in our case
    Dict = mp.Manager().dict()
    NUM_PERMUTATION = 256

    iterable = zip(repeat(Dict, len(k)), k)
    print(f'{time.time() - t1} secs was taken to initiate\n')

    t_start = time.time()

    print("Starting minhash + shingle creation....")
    # Let's start with the actual process of creating minhash and shingles
    with mp.Pool() as pool:
        pool.starmap(operation, iterable, chunksize=1000)

    # Pickling the minhash by creating a pickle dictionary
    # this dictionary contains all the hashValues from the minhash
    # as we cannot actually pickle object stored at some memory location
    pickle_dict = {}
    for key in tqdm(Dict.keys(), desc="pickling the minhash...."):
        pickle_dict[key] = Dict[key].hashvalues

    minhash_location = os.path.join(args['output'], 'hash_pickle.pc')
    with open(minhash_location, 'wb') as f:
        pickle.dump(pickle_dict, f)

    del pickle_dict
    print(f"Completed creating and indexing minhash in {time.time() - t_start} secs")
    # the process of minhash and its pickle is completely done

    # lsh is now initiated, we create a pickle file for it in the given directory
    # let's start the process
    lsh_location = os.path.join(args['output'], 'lsh_pickle.pc')

    lsh = MinHashLSH(threshold=0.90, num_perm=NUM_PERMUTATION, weights=(0.5, 0.5))
    with lsh.insertion_session() as session:
        for key in tqdm(Dict.keys(), desc="LSH processing"):
            session.insert(key=key, minhash=Dict[key])

    with open(lsh_location, 'wb') as f:
        pickle.dump(lsh, f)

    # so created and dumped the lsh file too

    print(f'pickle file saved at: {lsh_location}')
