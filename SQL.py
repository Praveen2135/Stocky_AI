import sqlite3
#Connecting to the data base
conn = sqlite3.connect("data.db")
c = conn.cursor()


def creat_table():
    c.execute('''CREATE TABLE IF NOT EXISTS ticker_data
              (tiker    TEXT
              date      DATE
              close     INT
              high      INT
              low       INT
              open      INT);''')
    print('Table created')

def add_data(ticker,date,close,high,low,open):
    c.execute('INSERT INTO ticker_data(ticker,date,close,high,low,open) VALUES (?,?,?,?,?,?)',(ticker,date,close,high,low,open))
    conn.commit()

def view_data():
    c.execute('SELECT * FROM tikerdata')
    data = c.fetchall()
    return data
