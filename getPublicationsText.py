from bs4 import BeautifulSoup
import json
from selenium import webdriver

DATA_IN_JSON = 'publications.json'
out_json = {}


if __name__ == '__main__':

    driver = webdriver.Firefox()

    # driver = webdriver.PhantomJS()
    # Get the publications
    with open(DATA_IN_JSON, 'r') as f:
        publications = json.load(f)
    i = 0
    for author in publications: 
        out_json[author] = {}
        for pub in publications[author]:
            try:
                print("Getting text for: " + pub['bib']['title'])
                url = pub['pub_url']
                driver.get(url)
                html = driver.page_source
                soup = BeautifulSoup(html)
                out_json[author][pub['bib']['title']] = soup.get_text()
            except Exception:
                print("Error getting text for: " + pub['bib']['title'])
        with open(f'publications_text_{author}.json', 'w') as f:
            json.dump(out_json, f, indent=4)
            out_json = {}
    driver.close()


            
            