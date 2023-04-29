import shutil

import xml.etree.ElementTree as ET
from os.path import exists

import py7zr
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

file1 = open('./data/file_list.text', 'r')
Lines = file1.readlines()

count = 0


def extract_content_files(file_1, tag):
    tree = ET.parse(file_1)
    root = tree.getroot()
    i = 1
    for ele in root:
        # print(ele.attrib['Body'])
        try:
            soup2 = BeautifulSoup(ele.attrib[tag], "html.parser")
            with open("./striped/" + line.strip() + str(i) + ".txt", "a") as my_file:
                my_file.write(soup2.get_text())
                my_file.write("\n")
            i += 1
        except MarkupResemblesLocatorWarning as e:
            print(e)


# Strips the newline character
for line in Lines:
    count += 1
    print("File{}: {}".format(count, line.strip()))
    archive = py7zr.SevenZipFile('./data/' + line.strip(), mode='r')
    archive.extractall(path="./tmp/")
    archive.close()

    file1 = './tmp/Posts.xml'
    file2 = './tmp/Comments.xml'
    if exists(file1):
        extract_content_files(file1, 'Body')
    if exists(file2):
        extract_content_files(file2, 'Text')
    try:
        shutil.rmtree("./tmp/")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))