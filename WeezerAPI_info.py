# from the Deezer API I am gathering data for: 
# rank (The track's Deezer rank)
# available_countries (List of countries where the track is available)
# release_date
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
cur.execute('''DROP TABLE IF EXISTS Weezer''')
cur.execute('''CREATE TABLE Weezer (title TEXT, rank INTEGER, countries INTEGER, release TEXT)''')

#each row returns a tuple of a song name and artist's name for that song
#We will use each tuple to gather the information we need from Weezer API
for row in rows:
    print("SEARCHING: ", row)
    #using this request to get the track id for a certain song so we can make a correct request (which requires the track id rather than the name)
    url = "https://api.deezer.com/search?q=track:\"{}\" artists:\"{}\"".format(row[0], row[1])
    reqs =  requests.get(url)
    #makes sure the request worked if the status code is 200
    if reqs.status_code == 200:
        data = json.loads(reqs.content)
        if len(data['data']) == 0:
            break
        
        best_match = data['data'][0]
        trackId = best_match['id']
        # now that I have the track id I will use it to make the correct request from the API to get the info I want
        newUrl = "https://api.deezer.com/track/{}".format(trackId)
        newReqs =  requests.get(newUrl)
        
        if newReqs.status_code == 200:
            info = json.loads(newReqs.content)
            
            

            if info == None:
                pass
            else:
                cur.execute('INSERT INTO Weezer (title, rank, countries, release) VALUES (?, ?, ?, ?)'
                , (info['title'], info['rank'], len(info['available_countries']), info['release_date']))
            
    else:
        print ("Error occured while fetching track information")
    
conn.commit()

# still need to figure out how to get the info for songs where the title from billboard doesnt exactly match the title on Weezer so the requests doesnt work