from scholarly import scholarly
import csv
import time
import json

JSON_FILE = 'data.json'
json_dict = {} # dictionary to store the data

if __name__ == "__main__":
    researcher_names=["jenifer doudna",
                        "Emmanuelle Charpentier",
                        "feng zhang",
                        "david liu",
                        "martin jinek",
                        "george church",
                        "francisco mojica",
                        "virginijus siksnys",
                        "stanley qi",
                        "matthew porteus"]
    for researcher_name in researcher_names:
        print("searching for researcher: ", researcher_name)
        search_query = scholarly.search_author(researcher_name)
        try: 
            author = scholarly.fill(next(search_query))
            scholarly.pprint(author)
            json_dict[researcher_name] = author
        except StopIteration:
            print("No results found for ", researcher_name)

    with open(JSON_FILE, 'w') as outfile:
        json.dump(json_dict, outfile)