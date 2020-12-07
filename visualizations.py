import sqlite3
import os
import requests
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objects as go

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
    numSongs = 8
    availCountries = (210, 189, 210, 208, 208, 208, 208, 208)

    # create plot
    index = np.arange(numSongs)
    bar_width = 0.3
    font_size = 5
    opacity = 0.75

    plt.bar(index, availCountries, bar_width, font_size, alpha=opacity, color='b', label='Num Countries')
    plt.ylabel('Number of Countries')
    plt.xlabel('Track Title')
    plt.title('Number of countries where the most popular tracks on Billboard are available')
    plt.xticks(index, ('Life Goes On', 'Mood', 'Dynamite', 'Positions', 'I Hope', 'Holy', 'Laugh Now Cry Later', 'Monster'))
    plt.show()

def makeBarGraph2():
    songs = ["Life Goes On", "Mood", "Dynamite", "Positions"]
    average_popularity = [6607.606557377049, 59825.5, 9779.826086956522, 248939.0] 
    index = np.arange(4)
    bar_width = 0.5
    font_size = 5
    opacity = 0.75
    color2 = ['green', 'yellow', 'blue', 'pink']
    plt.bar(index, average_popularity, bar_width, font_size, alpha=opacity, color= color2, label='Average Popularity')
    plt.ylabel('Average Popularity')
    plt.xlabel('Track Title')
    plt.title('Average Popularity for Top Four Songs on Billboard')
    plt.xticks(index, ("Life Goes On", "Mood", "Dynamite", "Positions"))
    plt.show()

def main(cur, conn):
    createBarChart()
    makeBarGraph2()
    createPieChart1(cur)
    conn.commit()
    
if __name__ == "__main__":
    main(cur, conn)

