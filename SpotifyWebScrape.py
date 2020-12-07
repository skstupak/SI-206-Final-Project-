import sqlite3
import os
import requests
import chart_studio.plotly as py
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import billboard
import matplotlib
import matplotlib.pyplot as plt

# the url to read from
url = "https://spotifycharts.com/regional/us/daily/2020-12-01"
def GetSoupObject(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup

soup = GetSoupObject(url)

# Dictionary of Top 200 Songs from 11-21-2020
def ScrapeSpotify(soup):
    top_200 = {}
    chart = soup.find('table', class_='chart-table')
    chart_list = chart.find_all('tr')
    # Loop through list of Top 200 Chart
    for song in chart_list[1:]:
    # Create the variable track_name
        track = song.find('td', class_='chart-table-track')
        track_name = track.strong.text
        if " (feat." in track_name:
            fixingsong = track_name.split("(feat.")
            fixed_song = fixingsong[0].strip()
            track_name = fixed_song
        if " (Feat." in track_name:
            fixingsong = track_name.split("(Feat.")
            fixed_song = fixingsong[0].strip()
            track_name = fixed_song
        if " (with" in track_name:
            fixingsong = track_name.split("(with")
            fixed_song = fixingsong[0].strip()
            track_name = fixed_song
        if " (" in track_name:
            fixingsong = track_name.split("(")
            fixed_song = fixingsong[0].strip()
            track_name = fixed_song
        if " -" in track_name:
            fixingsong = track_name.split(" -")
            fixed_song = fixingsong[0].strip()
            track_name = fixed_song
        if " [" in track_name:
            fixingsong = track_name.split(" [")
            fixed_song = fixingsong[0].strip()
            track_name = fixed_song
        track_name = track_name.title()
    # Create the variables artist_name, position_number, and streams_number 
        artist = song.find('td', class_='chart-table-track')
        artist_name = artist.span.text.strip('by ')
        position = song.find('td', class_='chart-table-position')
        position_number = position.text
        streams = song.find('td', class_='chart-table-streams')
        streams_number = streams.text
    # Make track_name the key for the top_200 dictionary with values artist_name, position_number, and streams_number
        top_200[track_name.strip()] = (artist_name.strip(), position_number.strip(), streams_number.strip())
    return top_200

spotify_dict = ScrapeSpotify(soup)

# Create a Spotify Top 200 table
dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + 'Billboard.db')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS SpotifyTop200''')
cur.execute('''CREATE TABLE SpotifyTop200 (title TEXT, artist TEXT, position INTEGER, streams INTEGER)''')

for song in spotify_dict:
    cur.execute('INSERT INTO SpotifyTop200 (title, artist, position, streams) VALUES (?, ?, ?, ?)', (song, spotify_dict[song][0], spotify_dict[song][1], spotify_dict[song][2]))
conn.commit()

# Loop through songs in Billboard database and create dictionary of the Spotify songs that are also in this database
dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + 'Billboard.db')
cur = conn.cursor()
cur.execute('''SELECT title FROM Billboard''')
titles = cur.fetchall()


# Create a Spotify table
cur.execute('''DROP TABLE IF EXISTS Spotify''')
cur.execute('''CREATE TABLE Spotify (title TEXT, artist TEXT, position INTEGER, streams INTEGER)''')

for title in titles:
    title = title[0]
    if title in spotify_dict.keys():
        cur.execute('INSERT INTO Spotify (title, artist, position, streams) VALUES (?, ?, ?, ?)', (title, spotify_dict[title][0], spotify_dict[title][1], spotify_dict[title][2]))
conn.commit()



def join_tables(cur, conn):
    cur.execute("SELECT Billboard.title, Spotify.title, Weezer.title FROM Billboard JOIN Spotify ON Billboard.title = Spotify.title JOIN Weezer ON Spotify.title = Weezer.title")
    t = cur.fetchall()
    conn.commit()
    return t 





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


