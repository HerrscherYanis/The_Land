import pyb
import time
import mfrc522

class RFID:
	def __init__(self):
		self.rdr = mfrc522.MFRC522('G18', 'G23', 'G19', 'G0', 'G5') #SCK, MOSI, MISO, RST, SDA
	def Read(self):
		while True:
			# Détecte la présence d'un badge
			(stat, tag_type) = self.rdr.request(self.rdr.REQIDL)				
			if stat == self.rdr.OK:
				(stat, raw_uid) = self.rdr.anticoll()
				if stat == self.rdr.OK:
					# Affichage du type de badge et de l'UID
					print("\nBadge détecté !")
					print(" - type : %03d" % tag_type)
					print(" - uid : %03d.%03d.%03d.%03d" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					# Affichage des données en mémoire
					if self.rdr.select_tag(raw_uid) == self.rdr.OK:
						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
						if self.rdr.auth(self.rdr.AUTHENT1A, 8, key, raw_uid) == self.rdr.OK:
							print(" - données : %s" % self.rdr.read(8))
							self.rdr.stop_crypto1()
						# Affichage en cas de problème
						else:
							print("Erreur de lecture")
					# Affichage en cas de problème
					else:
						print("Erreur badge")
	def Write(self):			
		while True:
			# Détecte la présence d'un badge
			(stat, tag_type) = self.rdr.request(self.rdr.REQIDL)				
			if stat == self.rdr.OK:
				(stat, raw_uid) = self.rdr.anticoll()
				if stat == self.rdr.OK:
					print("\nBadge détecté !")
					# Authentification
					if self.rdr.select_tag(raw_uid) == self.rdr.OK:
						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
						# Ecriture
						if self.rdr.auth(self.rdr.AUTHENT1A, 8, key, raw_uid) == self.rdr.OK:
							print("--> Ecriture en cours...")
							stat = self.rdr.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f") # Valeur hexa
							if stat == self.rdr.OK:
								print("--> Ecriture terminée !")
							else:
								print("--> Impossible d'écrire sur la carte !")
						# Affichage
						print("Données en mémoire : %s" % self.rdr.read(8))
						# Arrêt
						self.rdr.stop_crypto1()
				else:
					print("Erreur badge")
			time.sleep_ms(500)
			