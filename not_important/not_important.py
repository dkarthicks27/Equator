# import glob
# import time
# import pandas as pd
# import os
#
# os.remove("file.csv")
#
# start = time.time()
# fileList = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')  #instead of glob please insert list of all file path
# # also
# # doc_id = {list of document id}
# SHINGLE_SIZE = 3
# min_threshold = 0.90
# max_threshold = 0.95
# array = []
#
# def get_shingles(f, size):
#     shingles = set()
#     buf = f.read()  # read entire file
#     for i in range(0, len(buf) - size + 1):
#         yield buf[i:i + size]
#
#
# def jaccard(set1, set2):
#     x = len(set1.intersection(set2))
#     y = len(set1.union(set2))
#     return x / float(y)
#
#
# for i in range(0, len(fileList)):
#     for j in range(i, len(fileList)):
#         with open(fileList[i], errors="ignore") as f1, open(fileList[j], errors="ignore") as f2:
#             shingles1 = set(get_shingles(f1, size=SHINGLE_SIZE))
#             shingles2 = set(get_shingles(f2, size=SHINGLE_SIZE))
#         similarity = jaccard(shingles1, shingles2)
#         if min_threshold <= similarity <= max_threshold:
#             array.append((fileList[i], fileList[j], similarity))  # here instead of fileList[i] and fileList[j]
#             # insert doc_id[i] and doc_id[j]
#         if len(array) == 10000:
#             # print(len(array))
#             my_df = pd.DataFrame(array, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
#             with open('file.csv', 'a+') as csv_file:
#                 my_df.to_csv(path_or_buf=csv_file, index=False)
#                 array.clear()
#                 my_df = my_df.iloc[0:0]
#
#         # print(len(array))
#         if len(array) > 0:
#             my_df = pd.DataFrame(array, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
#             with open('file.csv', 'a+') as csv_file:
#                 my_df.to_csv(path_or_buf=csv_file, index=False)
#                 array.clear()
#                 my_df = my_df.iloc[0:0]


import multiprocessing as mp
import time
import cProfile

def multi(number):
    sum_sqr = 0
    for i in range(number):
        sum_sqr += i * i


def process_with_mp(numbers):
    start_time = time.time()
    with mp.Pool() as pool:
        pool.map(multi, numbers)
    end_time = time.time() - start_time
    print(f"It takes {end_time} secs with multiprocessing\n")


def process_without_mp(numbers):
    start_time = time.time()
    for i in numbers:
        multi(i)
    end_time = time.time() - start_time
    print(f"It takes {end_time} secs without multiprocessing")


if __name__ == '__main__':
    numbers = range(100)
    cProfile.run(process_with_mp(numbers))
    process_without_mp(numbers)