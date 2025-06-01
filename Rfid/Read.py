from mfrc522 import MFRC522 # https://github.com/danjperron/micropython-mfrc522
from utime import sleep, ticks_ms, ticks_diff
import json

class Scanner():
    def __init__(self, block):
        self.rc522 = MFRC522(spi_id=1,sck=18,miso=19,mosi=23,cs=5,rst=0)
        self.block = block
        self.key = [0xFF] * 6
        self.last_uid = None
        self.carte_here = False
        self.last_detection = 0

    def uidToString(self, uid):
        mystring = ""
        for i in uid:
            mystring = "%02X" % i + mystring
        return mystring
    
    def while_scan(self):
        while True:
            resp = self.scan()
            if resp != None:
                print(json.dumps(resp))
            else:
                print(None)
            sleep(1)

    def scan(self):
        print("Placez une carte RFID pres du lecteur.")
        (stat, tag_type) = self.rc522.request(self.rc522.REQIDL)

        if stat == self.rc522.OK:
            (stat, uid) = self.rc522.SelectTagSN()
            
            if stat == self.rc522.OK:
                current_uid = self.uidToString(uid)
                self.last_detection = ticks_ms()
            
                if self.carte_here == False or current_uid != self.last_uid:
                    self.carte_here = True
                    self.last_uid = current_uid
                
                    if self.rc522.auth(self.rc522.AUTHENT1A, self.block, self.key, uid) == self.rc522.OK:
                        (status, data) = self.rc522.read(self.block)
                        
                        self.rc522.stop_crypto1()
                        
                        if status == self.rc522.OK:
                            return {"uid" : current_uid, "data" : data}
                        else:
                            return None
                    else:
                        return None
        else:
            return None