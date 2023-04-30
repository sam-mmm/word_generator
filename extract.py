import os
import shutil
import sys
import uuid

import xml.etree.ElementTree as ET
from os.path import exists

import py7zr
import wget
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

source_text_files = "./data/source_text/"
if not exists(source_text_files):
    os.makedirs(source_text_files)

temp_folder = "./data/temp"
if not exists(temp_folder):
    os.makedirs(temp_folder)


def extract_content_files(file_1, tag):
    tree = ET.parse(file_1)
    root = tree.getroot()
    i = 1
    for ele in root:
        # print(ele.attrib['Body'])
        try:
            soup2 = BeautifulSoup(ele.attrib[tag], "html.parser")
            with open(source_text_files + str(uuid.uuid4()) + ".txt", "a") as my_file:
                my_file.write(soup2.get_text())
                my_file.write("\n")
            i += 1
        except MarkupResemblesLocatorWarning as e:
            print(e)


line = sys.argv[1]
print(line)
wget.download(line, out=temp_folder, bar=wget.bar_thermometer)
if "Posts" in line:
    path = temp_folder + "/Posts.xml"
    print(path)
    extract_content_files(path, 'Body')
    os.remove(path)
if "Comments" in line:
    path = temp_folder + "/Comments.xml"
    print(path)
    extract_content_files(path, 'Text')
    os.remove(temp_folder + "/Comments.xml")
