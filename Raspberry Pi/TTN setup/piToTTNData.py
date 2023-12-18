# Run this code in a terminal with sudo and then press RST on the LoRa board
import serial
ser = serial.Serial('/dev/ttyS0', 115200, timeout=3)
print(ser.name)

print("sending data")
ser.write(b'255,0,255,63,;')
print("Pi Sent: 1011")
x = ser.readline()
print(x.decode('utf-8'))
