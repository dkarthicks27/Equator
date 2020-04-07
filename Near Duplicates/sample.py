import os
from glob import glob
from sklearn.model_selection import train_test_split


arr = os.listdir(r'/Users/karthickdurai/Equator/OneDoc/')
filepath = '/Users/karthickdurai/Equator/OneDoc/*.txt'
file_list = glob(filepath)
x, z, y, w = train_test_split(arr, file_list, train_size=0.05)


# iterates over 3 lists and excutes
# 2 times as len(value)= 2 which is the
# minimum among all the three
for (a, b) in zip(x, y):
    print(a, b)
