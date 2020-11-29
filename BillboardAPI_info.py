#had to git clone the billboard.py repository and then run python setup.py install 
import billboard
import sqlite3
import os 
import json
c = billboard.ChartData('hot-100', date = '2020-11-21', year = None, fetch = True, timeout = 25)
title_lst = []
artist_lst = []
rank_lst = []
for rank in c:
    t = rank.title
    a = rank.artist
    r = rank.rank
    rank_lst.append(r)
    title_lst.append(t)
    artist_lst.append(a)


dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + 'Billboard.db')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Billboard''')
cur.execute('''CREATE TABLE Billboard (title TEXT, artist TEXT, rank INTEGER)''')

for i in range(len(title_lst)):
    cur.execute('INSERT INTO Billboard (title, artist, rank) VALUES (?, ?, ?)', (title_lst[i], artist_lst[i], rank_lst[i]))
conn.commit()