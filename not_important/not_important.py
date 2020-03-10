import pandas as pd
import numpy as np

# here we are going to see the data structures associated with pandas
# first one is Series
# Series is one dimensional labeled array capable of holding anything, the axis lables are collectively called as index

# a = pd.Series(data, index)
# here data refers to several things like python dictionary, or ndarray or simple scalar
# index is the list of axle labels
from numpy import NaN

arr1 = np.array([1, 2, 3, 4])
# upcasting arrays
arr2 = np.array([1, 2, 3.0])
# multidimensional arrays
arr3 = np.array([[1, 2], [3, 4]])
# minimum dimension 3
arr4 = np.array([1, 2, 3], ndmin=3)
# Type provided
arr5 = np.array([1, 2, 3], dtype=complex, ndmin=4)
x = np.array([(1, 2), (3, 4)], dtype=[('a', '<i4'), ('b', '<i4')], ndmin=2)
# print(arr1)
# print(arr2)
# print(arr3)
# print(arr4)
# print(arr5)
# print(x['a'],x['b'])


# now that we have understood np.arrays somewhat we will go into learning pd.series
# s = pd.Series(np.random.rand(5), ['a', 'b', 'c', 'd', 'e'])
# print(s)
# print(s.index)
# s1 = pd.Series(np.random.rand(5))
# print(s1)
# print(s1.index)
# it cna also be done in dict
b = {1: 10, 2: 5, 43: 120}
s = pd.Series(b)
# print(s)
# print(s.index)
# print(pd.Series(b, index=[2, 1, 10, 43]))
# it can also be a scalar value for which index must be provided
# print(s)

# now going on to data frame
d = {0: pd.Series([1, 2, 3, 4], ['a', 'b', 'c', 'd']), 1: pd.Series([2, 3, 4, 5], ['a', 'b', 'c', 'd']),
     2: pd.Series([1997, 1, 0, 3], ['a', 'b', 'c', 'd'])}
p = pd.DataFrame(d)
# print(p.columns)

# now we are looking at numpy.where()
# here we are trying to understand how numpy.where() works?

b = np.array([1, 2, -1, 3, 0, 5])
print(np.where(b > 1, b, NaN))
print(b)

x = pd.DataFrame([[1, 2], [[3, 4], 5]])
print(x)
