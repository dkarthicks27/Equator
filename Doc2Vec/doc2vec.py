import matplotlib.pyplot as plt
import numpy as np
import spacy
from sklearn.decomposition import PCA

nlp = spacy.load("en")
animals = "dog cat hamster lion tiger elephant cheetah monkey gorilla antelope rabbit mouse rat zoo home pet fluffy " \
          "wild domesticated "
animal_tokens = nlp(animals)
animal_vectors = np.vstack([word.vector for word in animal_tokens if word.has_vector])
pca = PCA(n_components=2)
animal_vecs_transformed = pca.fit_transform(animal_vectors)
x = np.c_[animals.split(), animal_vecs_transformed]
print(x)
plt.plot(animal_vecs_transformed, scalex=True, scaley=True)
plt.show()
animal_vecs_transformed = np.c_[animals.split(), animal_vecs_transformed]
