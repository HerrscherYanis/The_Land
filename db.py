import sqlite3 as sq

def DB_init():
    interact_DB("player.dbs", """create table if not exists player (id integer primary key autoincrement, uuid text, name text, life integer, strength integer, xp integer, level integer)""")
    
def interact_DB(name, arg, arg2=None):
    conn=sq.connect(name)
    if arg2 != None:
        conn.cursor().execute(arg, arg2)
    else:
        conn.cursor().execute(arg)
    ret = conn.cursor().fetchall()
    conn.commit()
    conn.close()
    return ret