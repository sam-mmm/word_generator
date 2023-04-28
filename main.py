import sys
import traceback

import requests
from bs4 import BeautifulSoup
import wget
from os.path import exists
import py7zr
import shutil
import spacy
import xml.etree.ElementTree as ET
import sqlite3
import json

con = sqlite3.connect("./build/words.db")
cur = con.cursor()

site = "https://archive.org/download/stackexchange"
r = requests.get(site)

nlp = spacy.load("en_core_web_md")

# converting the text
soup = BeautifulSoup(r.text, "html.parser")

for a in soup.find_all('a', href=True):
    href = a['href']
    if "meta" not in href and href.endswith(".7z"):
        url = site + "/" + href
        print(url)
        if not exists("./data/"+href):
            wget.download(url, out="./data", bar=wget.bar_thermometer)
        else:
            print("Already exists.")

        archive = py7zr.SevenZipFile('./data/' + href, mode='r')
        archive.extractall(path="./tmp/")
        archive.close()

        tree = ET.parse('./tmp/Posts.xml')
        root = tree.getroot()
        for ele in root:
            print(ele.attrib['Body'])
            soup2 = BeautifulSoup(ele.attrib['Body'], "html.parser")
            doc = nlp(soup2.get_text())

            for token in doc:
                print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                      token.shape_, token.is_alpha, token.is_stop)
                try:
                    cur.execute("CREATE TABLE IF NOT EXISTS " + token.pos_.lower() + "(word TEXT NOT NULL)")
                    res = cur.execute(
                        "SELECT count(*) FROM " + token.pos_.lower() + " WHERE word='" + token.text + "'")
                    count = res.fetchone()[0]
                    print("count:", count)
                    if count == 0:
                        cur.execute("INSERT INTO " + token.pos_.lower() + " VALUES('" + token.text + "')")
                        con.commit()
                    else:
                        print("count != 0")
                except sqlite3.Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print("Exception class is: ", er.__class__)
                    print('SQLite traceback: ')
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    print(traceback.format_exception(exc_type, exc_value, exc_tb))

        # Try to remove the tree; if it fails, throw an error using try...except.
        try:
            shutil.rmtree("./tmp/")

        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        print("\n")

stats = {}

res = cur.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'")
for row in res:
    for elem in row:
        print(elem)
        cur3 = con.cursor()
        res3 = cur3.execute("SELECT count(*) FROM " + elem.lower())
        count = res3.fetchone()[0]
        stats[elem] = count
        with open("./build/" + elem.lower() + ".txt", "a") as my_file:
            cur2 = con.cursor()
            data = cur2.execute("SELECT word FROM " + elem)
            for row2 in data:
                for elem2 in row2:
                    my_file.write(elem2)
                    my_file.write('\n')

            cur2.close()

stats_json = json.dumps(stats)  # note i gave it a different name
with open("./build/stats.json", "a") as my_file:
    my_file.write(stats_json)
