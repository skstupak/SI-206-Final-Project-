# from the Deezer API I am gathering data for: 
# rank (The track's Deezer rank)
# available_countries (List of countries where the track is available)
# release_date
import billboard
import sqlite3
import os 
import json
import requests


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
    cur.execute('''DROP TABLE IF EXISTS Weezer''')
    cur.execute('''CREATE TABLE Weezer (title TEXT PRIMARY KEY, rank INTEGER, countries INTEGER, release TEXT)''')

def join_tables(cur, conn):
    cur.execute("SELECT Weezer.title FROM Weezer JOIN Deezer ON Weezer.title = Deezer.title")
    t = cur.fetchall()
    return t 

#each row returns a tuple of a song name and artist's name for that song
#We will use each tuple to gather the information we need from Weezer API
def getRequest(cur):
    rows = getSongInfo(cur)
    for row in rows:
        #print("SEARCHING: ", row)
        #using this request to get the track id for a certain song so we can make a correct request (which requires the track id rather than the name)
        url = "https://api.deezer.com/search?q=track:\"{}\" artists:\"{}\"".format(row[0], row[1])
        reqs =  requests.get(url)
        #makes sure the request worked if the status code is 200
        if reqs.status_code == 200:
            data = json.loads(reqs.content)
            if len(data['data']) == 0:
                print (row)

                continue
            
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

def calculating_popularity(cur):
    cur.execute('SELECT rank FROM Weezer')
    r = cur.fetchall()
    cur.execute('SELECT weeks FROM Billboard')
    w = cur.fetchall()
    cur.execute('SELECT title FROM Billboard')
    t = cur.fetchall()
    d = {}
    for i in range(len(r)):
        if w[i] != 0:
            avg_pop = r[i][0]/w[i][0]
            d[t[i][0]] = avg_pop
    sorted_d = sorted(d.items(), key = lambda a: a[1], reverse = True)
    print(sorted_d)
    final = []
    for tup in sorted_d:
        final.append(tup[0])
    print(final)
    return final

def main():
    conn = getConnection('Billboard.db')
    cur = conn.cursor()
    makeTable(cur)
    getSongInfo(cur)
    getRequest(cur)
    calculating_popularity(cur)
    join_tables(cur, conn)
    conn.commit()
    
    
if __name__ == "__main__":
    main()

