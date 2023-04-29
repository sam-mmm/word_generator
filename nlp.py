from os import listdir
from os.path import isfile, join

import spacy

nlp = spacy.load("en_core_web_sm")

mypath = './striped'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for my_file in onlyfiles:
    print(my_file)
