import sqlite3 as sq
import uuid

def DB_init(name, life, strength, xp , level):
    interact_DB("player.dbs", """create table if not exists player (id integer primary key autoincrement, uuid text, name text, life integer, strength integer, xp integer, level integer)""")
    interact_DB("player.dbs", """INSERT INTO player (uuid, name,life,strength, xp, level )VALUES(?,?,?,?,?,?)""", (str(uuid.uuid4()), name, life, strength, xp, level))
    
def interact_DB(name, arg, arg2=None):
    conn=sq.connect(name)
    if arg2 != None:
        conn.cursor().execute(arg, arg2)
    else:
        conn.cursor().execute(arg)
    conn.commit()
    conn.close()