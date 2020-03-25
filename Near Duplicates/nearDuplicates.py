from sklearn.model_selection import train_test_split
from snapy import MinHash, LSH
from glob import glob
import os

filepath = '/Users/karthickdurai/Equator/OneDoc/*.txt'
file_list = glob(filepath)
# print(file_list)
files = os.listdir(r'/Users/karthickdurai/Equator/OneDoc/')
content = [
    'Jupiter is primarily composed of hydrogen with a quarter of its mass '
    'being helium',
    'Jupiter moving out of the inner Solar System would have allowed the '
    'formation of inner planets.',
    'A helium atom has about four times as much mass as a hydrogen atom, so '
    'the composition changes when described as the proportion of mass '
    'contributed by different atoms.',
    'Jupiter is primarily composed of hydrogen and a quarter of its mass '
    'being helium',
    'A helium atom has about four times as much mass as a hydrogen atom and '
    'the composition changes when described as a proportion of mass '
    'contributed by different atoms.',
    'Theoretical models indicate that if Jupiter had much more mass than it '
    'does at present, it would shrink.',
    'This process causes Jupiter to shrink by about 2 cm each year.',
    'Jupiter is mostly composed of hydrogen with a quarter of its mass '
    'being helium',
    'The Great Red Spot is large enough to accommodate Earth within its '
    'boundaries.'
]
files = files[:9]
minhash = MinHash(content, n_gram=9, permutations=100, hash_bits=64, seed=3)
lsh = LSH(minhash, files, no_of_bands=50)
print(lsh.query('485905.txt', min_jaccard=0.5))
# here min_jaccard is the threshold it will immediately return the near duplicates above that threshold.
# train, test, labelTrain, labelTest = train_test_split(file_list, train_size=0.05)
