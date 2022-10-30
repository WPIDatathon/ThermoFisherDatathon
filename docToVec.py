import os
import json
import gensim
import argparse

if __name__ == "__main__":
    # process the command line arguments

    # Load all of the data from the jsons in the publications_text folder
    # Then run the doc2vec model on it
    # Then save the model
    # Then save the vectors

    # Load the data
    data = {}
    for file in os.listdir("publications_text"):
        with open(os.path.join("publications_text", file), 'r') as f:
            data |= json.load(f)

    # Convert the data into a list of sentences
    # This is the format that gensim expects
    documents_raw = []
    titles = []
    for author in data:
        for title in data[author]:
            documents_raw.append(data[author][title].split())
            titles.append(title)

    # Print the first sentence
    # print(documents_raw[1])

    documents = [gensim.models.doc2vec.TaggedDocument(doc, [i]) for i, doc in enumerate(documents_raw)]
    # Create the model
    # if os.path.exists("doc2vec.model"):
        # model = gensim.models.doc2vec.Doc2Vec.load("doc2vec.model")
    # else:
    model = gensim.models.doc2vec.Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=32, epochs=100)
    model.save("doc2vec.model")

    titles = ["POROS 50 HQ Resin", "POROS XS Resin", "Pierce SAX Spin Columns", "POROS XQ Resin", "POROS 50 HQ Resin"]
    for title in titles:
        print(title)
        most_similar = model.docvecs.most_similar(model.docvecs[titles.index(title)])
        for i in most_similar:
            print(titles[i[0]])
        print()


    # Find the id for the title " Pierce SCX Spin Columns"
    # idx = titles.index("POROS 50 HQ Resin")
    # # Get the vector for the title " Pierce SCX Spin Columns"
    # vector = model.docvecs[idx]
    # # Find the most similar titles
    # sims = model.docvecs.most_similar(idx)
    # print(sims)
