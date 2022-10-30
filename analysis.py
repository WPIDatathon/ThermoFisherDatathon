import json 
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load in the data
    with open("out.json", 'r') as f:
        data = json.load(f)

    # Load in the publications
    with open("publications.json", 'r') as f:
        publications = json.load(f)

    with open("publications_text/product_corpus.json", 'r') as f:
        product_corpus = json.load(f)
    products = list(product_corpus["products"].keys())
    print(products)
    

    publications_to_citations_and_similarities = {}
    for product in products:
        print(f"Processing {product}")
        publications_to_citations_and_similarities[product] = {}
        for author in publications: 
            print(f"Processing {author}")
            for publication in publications[author]:
                # print(f"Processing {publication}")
                citations = publication["citations"]
                similarities = data[publication]["similarities"]
                publications_to_citations_and_similarities[product][publication] = {"citations": citations, "similarities": similarities}

    # Sort the publications by the number of citations and the similarity
    for product in products:
        publications_to_citations_and_similarities[product] = {k: v for k, v in sorted(publications_to_citations_and_similarities[product].items(), key=lambda item: (item[1]["citations"], item[1]["similarities"]), reverse=True)}
    
    # Print the top 10 publications for each product
    for product in products:
        print(f"Top 10 publications for {product}")
        for i, publication in enumerate(publications_to_citations_and_similarities[product]):
            if i < 10:
                print(f"\t{publication}: {publications_to_citations_and_similarities[product][publication]}")
            else:
                break
