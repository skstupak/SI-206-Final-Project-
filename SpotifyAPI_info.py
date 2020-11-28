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

