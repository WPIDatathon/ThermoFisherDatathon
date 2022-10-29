from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import json

DATA_IN_JSON = 'publications.json'

if __name__ == '__main__':
    # Get the publications
    with open(DATA_IN_JSON, 'r') as f:
        publications = json.load(f)

    # 
