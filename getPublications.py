from scholarly import scholarly
import csv
import time
import json

from multiprocessing import Pool
JSON_AUTHORS = 'data.json'
json_dict = {} # dictionary to store the data
json_out = {} # dictionary to store the data
JSON_OUT = 'publications.json'

def get_publication(publication):
    print("searching for publication: ", publication["bib"]["title"])
    try:
        return scholarly.fill(publication)
    except Exception as e:
        print("No results found for ", publication)
        print(e)
    return None

if __name__ == "__main__":
    with open(JSON_AUTHORS) as json_file:
        json_dict = json.load(json_file)
    for researcher_name in json_dict:
        print("searching for researcher: ", researcher_name)
        publications = json_dict[researcher_name]['publications']
        with Pool(16) as p:
            publications = p.map(get_publication, publications)
        json_out[researcher_name] = publications 
        with open(JSON_OUT, 'w') as outfile:
            json.dump(json_out, outfile)
    