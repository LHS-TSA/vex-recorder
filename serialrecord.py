import serial
import time

# port = serial.Serial("/dev/ttyUSB0", baudrate=115200)
port = serial.Serial("COM9", baudrate=115200)

while True:
    filename = "{}.txt".format(int(time.time()))
    with open(filename, 'w') as file:
        while True:
            res = port.readline().decode('ascii')
            print(res, end='')
            file.write("{0}".format(res))
            file.flush()
