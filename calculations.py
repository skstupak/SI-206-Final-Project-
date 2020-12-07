import sqlite3
import os
import requests

#calculations to txt file
fo = open('calculations.txt', 'w')
conn = sqlite3.connect('Billboard.db')
cur = conn.cursor()
d = {}
cur.execute('SELECT title FROM Billboard')
t = cur.fetchall()
cur.execute("SELECT position FROM Spotify")
p = cur.fetchall()
cur.execute('SELECT streams FROM Spotify')
s = cur.fetchall()
cur.execute('SELECT genres FROM Deezer')
g = cur.fetchall()
fo.write("The calculation shows the song title with the highest average popularity and it's genre" + '\n')
for i in range(len(p)):
    if p[i][0] != 0:
        y = ""
        for j in range(0, len(s[i][0])):
            if s[i][0][j] != ',':
                y += s[i][0][j]
        avg_pop = int(y)/p[i][0]
        d[t[i][0]] = (avg_pop, g[i][0])

sorted_d = sorted(d.items(), key = lambda a: a[1][0], reverse = True)
for tup in sorted_d:
    fo.write(tup[0] + ': ' + str(tup[1][0]) + ', ' + tup[1][1] + '\n')
