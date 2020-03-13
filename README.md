So there are several ways by which we can avoid loading the dataset to RAM or the memory:
	1. sklearn.datasets.load_files allows us to load text files as categories even from subfolders

so if we give the load content parameter to be false, then it doesnt really store in RAM.
	
	2. To conserve memory and clogging the ram when making a dictionary we could actually just read one line at a time from multiple documents.

This let's us to make processing quicker~ below exmaple shows it:
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.lower().split()

so the above class is an iterator which repeats until reaching EOF

So a beautifull refernce to it is:
https://www.machinelearningplus.com/nlp/gensim-tutorial/
