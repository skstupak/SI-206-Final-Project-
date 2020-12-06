import sqlite3
import os
import requests
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objects as go
from  plotly.offline import plot

dir = os.path.dirname(__file__) + os.sep
conn = sqlite3.connect(dir + 'Billboard.db')
cur = conn.cursor()

def createPieChart1(cur):
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

def createBarChart():
    # data to plot
    numSongs = 4
    availCountries = (210, 189, 210, 208)

    # create plot
    index = np.arange(numSongs)
    bar_width = 0.25
    opacity = 0.75

    plt.bar(index, availCountries, bar_width, alpha=opacity, color='b', label='Num Countries')
    plt.ylabel('Number of Countries')
    plt.xlabel('Track Title')
    plt.title('Number of countries where the most popular tracks on Billboard are available')
    plt.xticks(index, ('Life Goes On', 'Mood', 'Dynamite', 'Positions'))
    #plt.legend() this shows was each bar color means
    #plt.tight_layout()
    plt.show()

def makePieChart():
    songs = ["Life Goes On", "Mood", "Dynamite", "Positions"]
    average_popularity = [6607.606557377049, 59825.5, 9779.826086956522, 248939.0] 
    color2 = ['green', 'yellow', 'blue', 'pink']
    p2 = go.Pie(labels = songs, values = average_popularity, title = "Percent of Average Popularity for Top Four Songs on Billboard",
    hoverinfo = "label + value", textfont_size = 20, marker = dict(colors = color2))
    fig = go.Figure(p2)
    fig.show()
    py.iplot([p2], filename = 'average_popularity_songs', auto_open = True)

def main(cur, conn):
    createPieChart1(cur)
    createBarChart()
    makePieChart()
    conn.commit()
    
if __name__ == "__main__":
    main(cur, conn)

