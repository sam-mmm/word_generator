import shutil

import xml.etree.ElementTree as ET
import py7zr
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

file1 = open('./data/file_list.text', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    print("File{}: {}".format(count, line.strip()))
    archive = py7zr.SevenZipFile('./data/' + line.strip(), mode='r')
    archive.extractall(path="./tmp/")
    archive.close()

    tree = ET.parse('./tmp/Posts.xml')
    root = tree.getroot()
    i = 1
    for ele in root:
        # print(ele.attrib['Body'])
        try:
            soup2 = BeautifulSoup(ele.attrib['Body'], "html.parser")
            with open("./striped/"+line.strip()+str(i)+".txt", "a") as my_file:
                my_file.write(soup2.get_text())
                my_file.write("\n")
            i += 1
        except MarkupResemblesLocatorWarning as e:
            print(e)



    try:
        shutil.rmtree("./tmp/")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))