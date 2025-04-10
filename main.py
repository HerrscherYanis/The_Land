import class_file as cf
import db

screen = cf.Screen(640,480)
db.player_gen("df", 1, 21, 1, 0)
screen.start()