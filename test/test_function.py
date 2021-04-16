import os
from bs4 import BeautifulSoup
import requests
import json


text = 'Donald_Knuth'
with requests.get(f'https://fr.wikipedia.org/w/api.php?action=opensearch&search={text}') as r:
    url = json.loads(r.text)[3][0]
with requests.get(url) as r:
    soup = BeautifulSoup(r.text,'html.parser')
    print(soup)
