import sqlite3 as sq
#import random
import uuid

def init():
    interact("player.dbs", """create table if not exists player (id integer primary key autoincrement NOT NULL, uuid text NOT NULL, name text NOT NULL, life_current integer NOT NULL, life_max integer NOT NULL, strength integer NOT NULL, xp integer NOT NULL, level integer NOT NULL)""")
    interact("inventory.dbs", """create table if not exists inventory (id integer primary key autoincrement NOT NULL, name text)""")
    interact("enemy.dbs", """create table if not exists enemy (id integer primary key autoincrement NOT NULL, name text)""")
    interact("levelMap.dbs", """create table if not exists enemy (id integer primary key autoincrement NOT NULL, name text)""")
    
def interact(name, arg, arg2=None):
    conn=sq.connect("data/sql/"+name)
    if arg2 != None:
        conn.cursor().execute(arg, arg2)
    else:
        conn.cursor().execute(arg)
    ret = conn.cursor().fetchall()
    conn.commit()
    conn.close()
    return ret

def player_gen(name, life, strength, xp, level, uuid = uuid.uuid4()):
     interact("player.dbs", """INSERT INTO player (uuid, name,life_current,life_max,strength, xp, level )VALUES(?,?,?,?,?,?,?)""", (str(uuid), name,life, life, strength, xp, level))

