import os
import json
import gensim
import argparse

if __name__ == "__main__":
    # process the command line arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pub_folder', type=str, help='the folder of the data to process', default="publications_text")
    parser.add_argument('model_file', type=str, help='the model file to process', default="doc2vec.model")
    args = parser.parse_args()

    # Load all of the data from the jsons in the publications_text folder
    # Then run the doc2vec model on it
    # Then save the model
    # Then save the vectors

    # Load the data
    data = {}
    for file in os.listdir(args.pub_folder):
        with open(os.path.join(args.pub_folder, file), 'r') as f:
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
    if os.path.exists(args.model_file):
        model = gensim.models.doc2vec.Doc2Vec.load("doc2vec.model")
    else:
        model = gensim.models.doc2vec.Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=16, epochs=100)
        model.save("doc2vec.model")

    # Compare the first two sentences
    most_similar = model.docvecs.most_similar(1)
    print(most_similar)
    for i in most_similar:
        print(titles[i[0]])
