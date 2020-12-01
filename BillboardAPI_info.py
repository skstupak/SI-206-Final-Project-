#had to git clone the billboard.py repository and then run python setup.py install 
import billboard
import sqlite3
import os 
import json

#def billboard_lists():
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
#return ((title_lst, artist_lst, rank_lst))


#def db_setup(cur, conn):
dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + 'Billboard.db')
cur = conn.cursor()
#cur.execute('''DROP TABLE IF EXISTS Billboard''')
cur.execute('''CREATE TABLE IF NOT EXISTS Billboard (title TEXT, artist TEXT, rank INTEGER)''')
    

#def add_to_db(cur, conn):
count = 0 
    #t = []
    #for l in billboard_lists():
        #t.append(l[0])
for i in range(len(title_lst)):
    if count > 25:
        print('Retrieved 25 songs, restart to retrieve more')
        break 
    try:
        cur.execute('INSERT INTO Billboard (title, artist, rank) VALUES (?, ?, ?)', (title_lst[i], artist_lst[i], rank_lst[i]))
            #data = cur.fetchone()[0]
            #print('Found in database ', title)
            #continue
    except:
        pass
    count += 1
conn.commit()

#def main():
    #billboard_lists()
    #db_setup(cur, conn)
    #add_to_db(cur, conn)


#if __name__ == "__main__":
    #main()

#cur.execute('SELECT title FROM Billboard')
#lst = cur.fetchall()
#s = 0
#count = len(title_lst)
#new_list = []
#for i in title_lst:
#for s in range(25):
    #name = title_lst[s]
    #new_list.append(name)
    #creator = artist_lst[s]
    #number = rank_lst[s]
    #s += 1
    #if name not in new_list:
        #cur.execute('INSERT OR IGNORE INTO Billboard (title, artist, rank) VALUES (?, ?, ?)', (name, creator, number))
#print(new_list)
