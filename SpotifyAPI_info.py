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
print(sorted_d)
for tup in sorted_d:
    print(tup)
    fo.write(tup[0] + ': ' + str(tup[1][0]) + ', ' + tup[1][1] + '\n')


#visualization 1

BTSstream = 0
Drakestream = 0
KaneBrownstream = 0
LewisCapaldistream = 0
ArianaGrandestream = 0
for i in cur.execute("SELECT streams FROM Spotify WHERE artist = 'BTS'"):
    y = i[0].replace(',', '')
    streams = int(y)
    BTSstream += streams

for i in cur.execute("""SELECT streams FROM Spotify WHERE artist = 'Drake'"""):
    y = i[0].replace(',', '')
    streams = int(y)
    Drakestream += streams

for i in cur.execute("""SELECT streams FROM Spotify WHERE artist = 'Kane Brown'"""):
    y = i[0].replace(',', '')
    streams = int(y)
    KaneBrownstream += streams

for i in cur.execute("""SELECT streams FROM Spotify WHERE artist = 'Lewis Capaldi'"""):
    y = i[0].replace(',', '')
    streams = int(y)
    LewisCapaldistream += streams

for i in cur.execute("""SELECT streams FROM Spotify WHERE artist = 'Ariana Grande'"""):
    y = i[0].replace(',', '')
    streams = int(y)
    ArianaGrandestream += streams

l = ['BTS (Asian Music)', 'Drake (Rap/ Hip Hop)', 'Kane Brown (Country)', 'Lewis Capaldi (Alternative)', 'Ariana Grande (Pop)']
y_axis = [BTSstream, Drakestream, KaneBrownstream, LewisCapaldistream, ArianaGrandestream]
color = ['red', 'blue', 'green', 'yellow', 'purple']
p = go.Pie(labels = l, values = y_axis, title = "Number of Streams for Popular Artists in the Top Five Genres", 
            hoverinfo = 'label + value', textfont_size = 20, marker = dict(colors = color))
fig = go.Figure(p)
fig.show()
py.iplot([p], filename = 'streams_pop_genre', auto_open = True)

#visualization 2




