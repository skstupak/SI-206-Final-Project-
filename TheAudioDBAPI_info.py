# from the TheAudioDB API I am gathering data for: 
# strGenre
# intLoved
# intTotalListeners
# intTotalPlays
import billboard
import sqlite3
import os 
import json
import requests

API_KEY = "apiKey"

# pull top 100 from billboard to get a list of teack names and artists names 
dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + 'Billboard.db')
cur = conn.cursor()
cur.execute('''SELECT title, artist FROM Billboard''')
rows = cur.fetchall()


#creating a new table to write into and store the information we gather from the API
cur.execute('''DROP TABLE IF EXISTS TheAudioDB''')
cur.execute('''CREATE TABLE TheAudioDB (title TEXT, genre TEXT, loved INTEGER, totalListeners INTEGER, totalPlays INTEGER)''')

#each row returns a tuple of a song name and artist's name for that song
#We will use each tuple to gather the information we need from TheAudioDB API
for row in rows:
    url = "https://theaudiodb.com/api/v1/json/1/searchtrack.php?s={}&t={}".format(row[1], row[0])
    reqs =  requests.get(url)
    #makes sure the request worked if the status code is 200
    if reqs.status_code == 200:
        data = json.loads(reqs.content)
        #print (data)
        if data['track'] == None:
            pass
        else:
            cur.execute('INSERT INTO TheAudioDB (title, genre, loved, totalListeners, totalPlays) VALUES (?, ?, ?, ?, ?)'
            , (data['track'][0]["strTrack"], data['track'][0]["strGenre"], data['track'][0]["intLoved"], data['track'][0]["intTotalListeners"], data['track'][0]["intTotalPlays"]))
            
    else:
        print ("Error occured while fetching track information")
    
conn.commit()


# still need to figure out how to get the info for songs where the title from billboard doesnt exactly match the title on audioDB so the requests doesnt work

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def createSimpleBarChart():
    height = [210, 189, 210, 208, 208, 208]
    songs = ('Life Goes On', 'Mood', 'Dynamite', 'Positions', 'I Hope', 'Holy')
    #bar_height = np.arange(height)
    countries = [250,200,150,100,50,0]

    plt.bar(height, countries, align='center', alpha=0.75)
    plt.xticks(height, songs)
    plt.ylabel('Track Title')
    plt.xlabel('Number of Countries')
    plt.title('Number of countries where the most popular tracks on Billboard are available')

    plt.show()

def createBarChart():
    # data to plot
    n_groups = 4
    availCountries = (210, 189, 210, 208)
    

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.75

    rects1 = plt.bar(index, availCountries, bar_width,
    alpha=opacity,
    color='b',
    label='Num Countries')

    plt.ylabel('Number of Countries')
    plt.xlabel('Track Title')
    plt.title('Number of countries where the most popular tracks on Billboard are available')
    plt.xticks(index + bar_width, ('Life Goes On', 'Mood', 'Dynamite', 'Positions'))
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    createBarChart()
    
if __name__ == "__main__":
    main()

