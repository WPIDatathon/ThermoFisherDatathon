import os
import json
import gensim
import argparse
import nltk

if __name__ == "__main__":
    # process the command line arguments

    # Load the data
    data = {}
    for file in os.listdir("publications_text"):
        with open(os.path.join("publications_text", file), 'r') as f:
            data |= json.load(f)

    documents_raw = []
    titles = []
    for author in data:
        for title in data[author]:
            text = data[author][title]
            # Remove the stopwords
            text = [word for word in text if word not in nltk.corpus.stopwords.words('english')]
            # Lemmatize the words
            text = [nltk.stem.WordNetLemmatizer().lemmatize(word) for word in text]
            documents_raw.append(text)
            titles.append(title)

    documents = [gensim.models.doc2vec.TaggedDocument(doc, [i]) for i, doc in enumerate(documents_raw)]

    model = gensim.models.doc2vec.Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=32, epochs=100)
    model.save("doc2vec.model")

    titles_to_search = ["POROS 50 HQ Resin", "POROS XS Resin", "Pierce SAX Spin Columns", "POROS XQ Resin", "POROS 50 HQ Resin"]
    for title in titles_to_search:
        print(title)
        most_similar = model.docvecs.most_similar(model.docvecs[titles.index(title)])
        for i in most_similar:
            print(titles[i[0]])
        print()