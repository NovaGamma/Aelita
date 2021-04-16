import os
import json
from difflib import SequenceMatcher

with open('cleaned3.json','r') as file:
    names = json.load(file)

array = []

n = 0

for name in names:
    n+=1
    print(f'{n} : {name}')
    if 'youtube' in name:
        array.append(name)
        continue
    found = False
    for i in array:
        if SequenceMatcher(None,name,i).ratio() > 0.8:
            found = True
            break
    if not found:
        array.append(name)



with open('cleaned4.json','w') as file:
    json.dump(array,file)
