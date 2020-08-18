import time
import concurrent.futures
from glob import glob
import pandas as pd
import gc

t1 = time.time()

#
# def func(seconds):
#     print(f"Sleeping {seconds} secs...")
#     time.sleep(seconds)
#     return "Done sleeping..."
#     # print("Done sleeping...")


# processes = []
# for _ in range(10):
#     p = mp.Process(target=func, args=[2])
#     p.start()
#     processes.append(p)
#
# for process in processes:
#     process.join()

filePath = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
filePath = filePath[:100]
# size = 2
#
#
# def get_shingles(file):
#     print(f"Getting shingles started...")
#     t = time.time()
#     time.sleep(1)
#     with open(file=file, errors="ignore") as file:
#         buf = file.read()  # read entire file
#         for y in range(0, len(buf) - size + 1):
#             pass
#     return f"getting shingles completed in {time.time() - t} secs"
#
#
# # for files in filePath:
# #     result = get_shingles(files, 2)
# #     print(result)
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     f1 = executor.map(get_shingles, filePath)
#
# print(f"It took {round(time.time() - t1, 2)} secs to complete")



d = []

for i, file in enumerate(filePath):
    d.append((i, file))
    if len(d) == 10:
        x = pd.DataFrame(d, columns=['doc_id', 'filepath'])
        print(x)
        print("\n")
        with open('dummy.csv', 'a+') as csv:
            x.to_csv(path_or_buf=csv, index=False)
            d.clear()
            del x
        print(x)

# print(d)
# x = pd.DataFrame(d, columns=['doc_id', 'filepath'])
# print(x)
# del x
# gc.collect()
