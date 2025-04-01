import class_file as cf

screen = cf.Screen(500,500)
plat = cf.Object(cf.Image('./resources/Error.jpg', 100, 100), 0, 0)
screen.get("petit_image", plat)
screen.start()