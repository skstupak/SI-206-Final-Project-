import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import billboard

# the url to read from
url = "https://spotifycharts.com/regional/global/daily/2020-11-21"
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

def FixSongs(spotify_dict):
    for song in spotify_dict.keys():
        if " (feat." in song:
            fixingsong = song.split("(feat.")
            fixed_song = fixingsong[0].strip()
            song = fixed_song
        if " (Feat." in song:
            fixingsong = song.split("(Feat.")
            fixed_song = fixingsong[0].strip()
            song = fixed_song
        if " (with" in song:
            fixingsong = song.split("(with")
            fixed_song = fixingsong[0].strip()
            song = fixed_song
        if " (" in song:
            fixingsong = song.split("(")
            fixed_song = fixingsong[0].strip()
            song = fixed_song
        song = song.title()
    return spotify_dict

fixed_dict = FixSongs(spotify_dict)
spotify_keys = fixed_dict.keys()      

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
    if title in spotify_keys:
        cur.execute('INSERT INTO Spotify (title, artist, position, streams) VALUES (?, ?, ?, ?)', (title, fixed_dict[title][0], fixed_dict[title][1], fixed_dict[title][2]))
conn.commit()
        

    


