import serial
import time

# Remplace 'COM3' par ton port (ex: '/dev/ttyUSB0' sur Linux)
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)  # attendre que l'ESP32 démarre

# Envoyer une commande
ser.write(b'HELLO\n')

# Lire la réponse
while True:
    if ser.in_waiting:
        ligne = ser.readline().decode('utf-8').strip()
        print("ESP32 a répondu:", ligne)
        break

ser.close()