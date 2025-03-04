import sqlite3 as sq

class Data:
    conn=sq.connect("player.dbs")
    conn.cursor().execute("""create table if not exists player 
    (id integer primary key autoincrement, nom text)""")
    conn.close()