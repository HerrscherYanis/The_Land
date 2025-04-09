import sqlite3 as sq
import random

def DB_init(name, life, strength, xp , level):
    interact_DB("player.dbs", False, """create table if not exists player (id integer primary key autoincrement, uuid text, name text, life integer, strength integer, xp integer, level integer)""")
    interact_DB("player.dbs", True , f"""INSERT INTO player (uuid, name,life,strength, xp, level )VALUES({iduu()},{name},{life},{strength},{xp},{level})""")
    
def interact_DB(name, type, arg):
    conn=sq.connect(name)
    conn.cursor().execute(arg)
    if type == "set" or type == True:
        conn.commit()
    conn.close()

def iduu():
    idu = ""

    for x in range(8):
        idu = idu + str(random.randint(0, 9))

    print(idu)
    return idu