from os.path import exists

import requests
import wget
from bs4 import BeautifulSoup

site = "https://archive.org/download/stackexchange"
r = requests.get(site)

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

        with open("./data/file_list.text", "a") as my_file:
            my_file.write(href)
            my_file.write("\n")

        print("\n")