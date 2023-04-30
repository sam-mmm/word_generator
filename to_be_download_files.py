import os
from os.path import exists

import requests
import wget
from bs4 import BeautifulSoup

data_file = "./data/file_list.text"
if not exists("./data"):
    os.makedirs("./data")

site = "https://archive.org/download/stackexchange"
r = requests.get(site)
soup = BeautifulSoup(r.text, "html.parser")
anchors = soup.find_all('a', href=True);
print(len(anchors))


for a in anchors:
    href = a['href']
    if "meta" not in href and a.text.__contains__("View Contents"):
        url = site + "/" + href
        print(url)
        r1 = requests.get(url)
        soup1 = BeautifulSoup(r1.text, "html.parser")
        for a1 in soup1.find_all('a', href=True):
            if a1["href"].endswith("Comments.xml") or a1["href"].endswith("Posts.xml"):
                print(a1)
                path = a1["href"]
                if not path.startswith("https:"):
                    path = "https:" + path
                with open(data_file, "a") as my_file:
                    my_file.write(path)
                    my_file.write("\n")

        print("\n")