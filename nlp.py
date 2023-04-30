import sqlite3
import sys
import traceback
from os import listdir
from os.path import isfile, join

import spacy

file = sys.argv[1]
print(file)
# print(f"Arguments count: {len(sys.argv)}")
# for i, arg in enumerate(sys.argv):
#     print(f"Argument {i:>6}: {arg}")

con = sqlite3.connect("./data/words.db")
cur = con.cursor()
nlp = spacy.load("en_core_web_sm")

nlp_text = ""
with open(file) as f:
    for line in f:
        nlp_text += line

doc = nlp(nlp_text)

for token in doc:
    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #       token.shape_, token.is_alpha, token.is_stop)
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS " + token.pos_.lower() + "(word TEXT NOT NULL)")
        sql2 = "SELECT count(*) FROM " + token.pos_.lower() + " WHERE word = ?"
        res = cur.execute(sql2, (token.text,))
        count = res.fetchone()[0]
        # print("count:", count)
        if count == 0:
            cur.execute("INSERT INTO " + token.pos_.lower() + " VALUES(?)", (token.text,))
            con.commit()
        # else:
        #     print("count != 0")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQL2:',sql2)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

print("Done,", file, "\n", nlp_text)
