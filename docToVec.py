import os
import json
import gensim
import argparse
import nltk
import re
from multiprocessing import Pool
import pickle
import numpy as np

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove new line characters
    text = text.replace("\\n", " ")
    # Remove all duplicate whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = text.split(" ")
    # Remove the stopwords
    text = [word for word in text if word not in nltk.corpus.stopwords.words('english')]
    # Lemmatize the words
    text = [nltk.stem.WordNetLemmatizer().lemmatize(word) for word in text]
    return text


if __name__ == "__main__":
    # process the command line arguments

    # Load the data
    data = {}
    for file in os.listdir("publications_text"):
        with open(os.path.join("publications_text", file), 'r') as f:
            data |= json.load(f)
        print("Loaded %d documents" % len(data))

    if os.path.exists("documents_raw.pickle") and os.path.exists("titles.pickle"):
        with open("documents_raw.pickle", 'rb') as f:
            documents_raw = pickle.load(f)
        with open("titles.pickle", 'rb') as f:
            titles = pickle.load(f)
    else:
        documents_raw = []
        titles = []
        for author in data:
            print(f"Processing {author}")
            with Pool(16) as p:
                documents_raw += p.map(clean_text, data[author].values())
            titles += list(data[author].keys())
        
        # Write the documents to a file 
        with open("documents_raw.pickle", 'wb') as f:
            pickle.dump(documents_raw, f)

        # Write the titles to a file
        with open("titles.pickle", 'wb') as f:
            pickle.dump(titles, f)

    # Write the documents to a file
    print(documents_raw[0])
    print("Length of documents: %d" % len(documents_raw))
    
    documents = [gensim.models.doc2vec.TaggedDocument(doc, [i]) for i, doc in enumerate(documents_raw)]

    if os.path.exists("model.pickle"):
        print("Loading model")
        model = pickle.load(open("model.pickle", 'rb'))
    else:
        print("Training the model")
        model = gensim.models.doc2vec.Doc2Vec(documents, workers=16, vector_size=100, window=5, min_count=1, epochs=100)
        pickle.dump(model, open("model.pickle", 'wb'))

    titles_to_search = ["Pierce SCX Spin Columns", "POROS XS Resin", "Pierce SAX Spin Columns", "POROS XQ Resin", "POROS 50 HQ Resin"]
    documents_vec = [model.infer_vector(doc) for doc in documents_raw]
    titles_to_search_index = [titles.index(title) for title in titles_to_search]
    titles_to_search_vec = [documents_vec[i] for i in titles_to_search_index]
    print(titles_to_search_index)
    out_json = {}
    for doc_vec, title in zip(documents_vec, titles):
        print(title)
        out_json[title] = {}
        for i, j in zip(titles_to_search_vec, titles_to_search):
            # Find the cosine similarity
            print(j, np.dot(doc_vec, i) / (np.linalg.norm(doc_vec) * np.linalg.norm(i)))
            out_json[title][j] = float(np.dot(doc_vec, i) / (np.linalg.norm(doc_vec) * np.linalg.norm(i)))
        print("")
    with open("out.json", 'w') as f:
        json.dump(out_json, f, indent=4)


    # search_vec = [model.infer_vector(titles.index(title_to_search)) for title_to_search in titles_to_search]
    # print(search_vec)
    # for title in titles_to_search:
    #     print(title)
    #     most_similar = model.docvecs.most_similar(model.docvecs[titles.index(title)])
    #     for i in most_similar:
    #         print(titles[i[0]])
    #     print()