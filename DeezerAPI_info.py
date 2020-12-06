# from the Deezer API I am gathering data for: 
# genre
import billboard
import sqlite3
import os 
import json
import requests
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# getting cursor to be used for the rest of the code
def getConnection(database):
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + database)
    return conn

# pull top 100 from billboard to get a list of teack names and artists names 
def getSongInfo(cur):
    cur.execute('''SELECT title, artist FROM Billboard''')
    rows = cur.fetchall()
    return rows


#creating a new table to write into and store the information we gather from the API
def makeTable(cur):
    cur.execute('''DROP TABLE IF EXISTS Deezer''')
    cur.execute('''CREATE TABLE Deezer (title TEXT, genres TEXT)''')

def makeRequest(url):
    reqs = requests.get(url)

    if reqs.status_code == 200:
        return (json.loads(reqs.content))

    else:
        return None

#each row returns a tuple of a song name and artist's name for that song
#We will use each tuple to gather the information we need from Weezer API
def getRequest(cur):
    rows = getSongInfo(cur)
    for row in rows:
        #using this request to get the track id for a certain song so we can make a correct request (which requires the track id rather than the name)
        url = "https://api.deezer.com/search?q=track:\"{}\" artists:\"{}\"".format(row[0], row[1])
        trackData = makeRequest(url)
        if len(trackData['data']) == 0 or trackData == None:
            print (row)
            continue
            
        best_match = trackData['data'][0]
        trackId = best_match['id']
            
            

 
        # now that I have the track id I will use it to get the album id
        newUrl = "https://api.deezer.com/track/{}".format(trackId)
        albumData = makeRequest(newUrl)
        if albumData == None:
            continue
        albumId = albumData['album']['id']
                
                
        # now that I have the album id I will you it to make an api album data request to get the genre        
        nextUrl = "https://api.deezer.com/album/{}".format(albumId)
        genre = makeRequest(nextUrl)
     
        
        genreList = ",".join([g['name'] for g in genre['genres']['data']])                
        if len(genreList) == 0:
            genreList = 'Holiday'    

        if genre == None:
            pass
        else:
            cur.execute('INSERT INTO Deezer (title, genres) VALUES (?, ?)'
            , (best_match['title'], genreList))

                

def main():
    conn = getConnection('Billboard.db')
    cur = conn.cursor()
    makeTable(cur)
    getSongInfo(cur)
    getRequest(cur)
    conn.commit()
    
if __name__ == "__main__":
    main()

