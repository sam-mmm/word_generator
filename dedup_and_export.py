import json
import os
import sqlite3
from os.path import exists

data_file = "./data/export/"
if not exists(data_file):
    os.makedirs(data_file)

con = sqlite3.connect("./data/words.db")
cur = con.cursor()

stats = {}

res = cur.execute(
    "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_deduplicated%'")
for row in res:
    for elem in row:
        print(elem)
        cur3 = con.cursor()
        res3 = cur3.execute("CREATE TABLE IF NOT EXISTS " + elem.lower()+"_deduplicated AS select distinct * from "+elem.lower())
        res3 = cur3.execute("SELECT count(*) FROM " + elem.lower()+"_deduplicated")
        count = res3.fetchone()[0]
        stats[elem] = count
        with open(data_file + elem.lower() + ".txt", "a") as my_file:
            cur2 = con.cursor()
            data = cur2.execute("SELECT word FROM " + elem)
            for row2 in data:
                for elem2 in row2:
                    my_file.write(elem2)
                    my_file.write('\n')

            cur2.close()

stats_json = json.dumps(stats)  # note i gave it a different name
with open("./data/export/stats.json", "a") as my_file:
    my_file.write(stats_json)
