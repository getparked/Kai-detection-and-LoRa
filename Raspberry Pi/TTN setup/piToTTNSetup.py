# Run this code in a terminal with sudo and then press RST on the LoRa board
import serial
ser = serial.Serial('/dev/ttyS0', 115200, timeout=3)
print(ser.name)
X = ''
while not X == 'Connected to TTN!\n':
    x = ser.readline()
    X = x.decode('utf-8')
    print(X)
    
print("sending data")
ser.write(b'12,123,321,21,255,55,;')
print("data sent")
x = ser.readline()
print(x.decode('utf-8'))
