Some important tips:

For filtering the tokens:

dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)


Now let's understand the terminology:

filter out tokens that appear in less than 15 documents and more than 0.5 docs or half of a document, 

keep only the first 100000 most frequent tokens.


so we can define no_below, no_above and keep_n according to our requirements.
