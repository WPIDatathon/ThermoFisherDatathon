import gensim
import os
import json

if __name__ == "__main__":
    # Load the model
    model = gensim.models.doc2vec.Doc2Vec.load("doc2vec.model")

    