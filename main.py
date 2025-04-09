import class_file as cf

screen = cf.Screen(640,480)
screen.interact_DB("player.dbs", False, """create table if not exists player (id integer primary key autoincrement, name text, life integer, strength integer, xp integer, level integer)""")
screen.interact_DB("player.dbs", True , """INSERT INTO player (name,life,strength, xp, level )VALUES('y', 19, 8, 1, 0)""")
screen.start()