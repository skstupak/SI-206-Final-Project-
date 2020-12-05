#had to git clone the billboard.py repository and then run python setup.py install 
import billboard
import sqlite3
import os 
import json
import chart_studio.plotly as py
import plotly.graph_objects as go

def db_setup(db_name):
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + 'Billboard.db')
    cur = conn.cursor()
    return cur, conn

def get_data():
    c = billboard.ChartData('hot-100', date = '2020-12-01', year = None, fetch = True, timeout = 25)
    return c

def create_database():
    title_lst = []
    artist_lst = []
    rank_lst = []
    week_lst = []
    c = get_data()
    for rank in c:
        t = rank.title
        a = rank.artist
        r = rank.rank
        w = rank.weeks
        rank_lst.append(r)
        title_lst.append(t)
        artist_lst.append(a)
        week_lst.append(w)
    cur, conn = db_setup('Billboard.db')
    cur.execute('''CREATE TABLE IF NOT EXISTS Billboard (title TEXT, artist TEXT, rank INTEGER, weeks INTEGER)''')
    count = 0
    for i in range(len(title_lst)):
        if count > 24:
            break
        if cur.execute('SELECT title FROM Billboard WHERE title = ? AND artist = ? AND rank = ? AND weeks = ?', (title_lst[i], artist_lst[i], rank_lst[i], week_lst[i])).fetchone() == None:
            cur.execute('INSERT INTO Billboard (title, artist, rank, weeks) VALUES (?, ?, ?, ?)', (title_lst[i], artist_lst[i], rank_lst[i], week_lst[i]))
            count += 1

    conn.commit()

    # Data for pie chart #2
songs = ["Life Goes On", "Mood", "Dynamite", "Positions"]
average_popularity = [6607.606557377049, 59825.5, 9779.826086956522, 248939.0] 
color2 = ['green', 'yellow', 'blue', 'pink']
p2 = go.Pie(labels = songs, values = average_popularity, title = "Percent of Average Popularity for Top Four Songs on Billboard",
hoverinfo = "label + value", textfont_size = 20, marker = dict(colors = color2))
fig = go.Figure(p2)
fig.show()
py.iplot([p2], filename = 'average_popularity_songs', auto_open = True)


def main():
    create_database()


if __name__ == "__main__":
    main()

