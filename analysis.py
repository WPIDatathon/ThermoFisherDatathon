import contextlib
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
                title = publication["bib"]["title"]
                print(f"Processing {title}")
                citations = publication["num_citations"]
                with contextlib.suppress(KeyError):
                    similarities = data[title][product]
                    print(similarities)
                    publications_to_citations_and_similarities[product][title] = {"citations": citations, "similarities": similarities}
                    

    # Convert to a csv file
    with open(f"analysis/citations_and_similarities.csv", 'w') as f:
        f.write("Product,Title,Citations,Similarities\n")
        for product in products:
            for title in publications_to_citations_and_similarities[product]:
                f.write(f"\"{product}\",\"{title}\",\"{publications_to_citations_and_similarities[product][title]['citations']}\",\"{publications_to_citations_and_similarities[product][title]['similarities']}\"\n")
    

    # publications_to_citations_and_similarities_sorted = {}
    # # Sort the publications by the number of citations
    # for product in products:
    #     # for publication in publications_to_citations_and_similarities[product]:
    #         # print(publication)
    #         # print(publications_to_citations_and_similarities[product][publication])
    #         # print()
    #     publications_to_citations_and_similarities_sorted[product] = sorted(publications_to_citations_and_similarities[product].items(), key=lambda x: x[1]["citations"], reverse=True)
    #     for publication in publications_to_citations_and_similarities_sorted[product]:
    #         print(publication)
    #         print()
    #     print()
    
    # # Find the max number of citations for each product
    # max_citations = {}
    # for product in products:
    #     print(f"Processing {product}")
    #     max_citations[product] = publications_to_citations_and_similarities[product]
    #     print(max_citations[product])

    # Print the top 10 publications for each product
    # for product in products:
    #     print(f"Top 10 publications for {product}")
    #     for i, publication in enumerate(publications_to_citations_and_similarities[product]):
    #         if i < 10:
    #             print(f"\t{publication}: {publications_to_citations_and_similarities[product][publication]}")
    #         else:
    #             break
