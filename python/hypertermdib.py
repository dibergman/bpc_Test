import serial
#import matplotlib.pyplot as plt
import time
import numpy as np
import struct
import sys

ser_port = sys.argv[1]
ser = serial.Serial(ser_port, 115200, timeout=10)
#np.set_printoptions(precision=3, suppress = True)


while True:
	try:
		data = ser.read()
		#print(data.decode('UTF-8'), end='')
		sys.stdout.write(data.decode('UTF-8'))
		sys.stdout.flush()
		
	except KeyboardInterrupt:
		ser.close()
		sys.exit()


