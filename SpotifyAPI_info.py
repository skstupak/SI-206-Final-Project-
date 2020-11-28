import sqlite3
import os
import requests
from bs4 import BeautifulSoup

# the url to read from
url = "https://spotifycharts.com/regional/global/daily/2020-11-21"

resp = requests.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')

# Dictionary of Top 200 Songs from 11-21-2020
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

# Loop through songs in Billboard database and create dictionary of the Spotify songs that are also in this database

    


