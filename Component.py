import serial
import time
from db import interact, uuid_view
import json

class Communication():
	def __init__(self, com="COM3"):
		self.com = com
	
	def SendBack(self):
		ser = serial.Serial(self.com, 115200, timeout=1)
		time.sleep(2)

		while ser.in_waiting:
			line = ser.readline().decode().strip()
		try:
			data = json.loads(line)
			print(data)
			if uuid_view(data.get("uid")) == True:
				interact("player.dbs", """INSERT INTO player (uuid, name,life_current,life_max,strength, xp, level )VALUES(?,?,?,?,?,?,?)""", (data.get("uid"), "Default",data.get("data")[0], data.get("data")[1], data.get("data")[2], data.get("data")[3], data.get("data")[4]))
				print("True")
		except json.JSONDecodeError:
			print("False")
df = Communication()
df.SendBack()