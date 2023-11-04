import sqlite3

def search():

    connection = sqlite3.connect("intramural.sqlite")
    crsr = connection.cursor()

    query = "SELECT * FROM games "

    crsr.execute(query)
    search = crsr.fetchall()
    print(search)

search()