import glob
from tqdm import tqdm
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


def get_shingles(f, size):
    shingles = set()
    buf = f.read()  # read entire file
    for i in range(0, len(buf) - size + 1):
        yield buf[i:i + size]



if __name__ == '__main__':
    fileList = glob.glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
    print(len(fileList))
    if '/Users/karthickdurai/Equator/OneDoc/85.txt' in fileList:
        print(True)