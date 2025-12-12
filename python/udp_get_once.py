#import matplotlib.pyplot as plt
import socket
import time
import numpy as np
import struct
import sys
import os
from os import system

#message "Loop" needed to get data from server
message = b"Loop"
np.set_printoptions(precision=3, suppress = True)

IP = sys.argv[1]
model = sys.argv[2]
serial = sys.argv[3]
chan = sys.argv[4]

modelname = "%s_%s" % (model,serial)
filename = "%s_%s_CH%s_udp_hk.txt" %(model, serial, chan)
filepath = "./_temp/"


try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(2)
	server_address = (IP, 5000)

except Exception as err:
	print("Socket error: %s" % err)


try:
	
	
	sock.sendto(message, server_address)
	data, addr = sock.recvfrom(2048)
	w = np.asarray(struct.unpack('<60f', data))

	fp = open(filepath+filename, 'w')
	fp.write("UDP Housekeeping Data for LT-EL-SR-PS-CRR-%s S/N %s\n\n" \
	         % (model, serial) )
	fp.write("Full power data for CH%s\n" % chan)         
			
	for j in range(60):
		if j == 0:
			fp.write("\n 1. ")
		if j == 1:
			fp.write("\n 2. ")
		if j == 7:
			fp.write("\n 8. ")
		if j == 13:
			fp.write("\n14. ")
		if j == 18:
			fp.write("\n19. ")
		if j == 26:
			fp.write("\n27. ")
		if j == 35:
			fp.write("\n36. ")
		if j==44:
			fp.write("\n45. ")
		if j==52:
			fp.write("\n53. ")
		if j==54:
			fp.write("\n55. ")
		if j==59:
			fp.write("\n60. ")
			
		if j < 18: 
			s = ("%8.1f" % w[j])
			fp.write(s)
		if j >= 18 and j < 35:
			s = ("%8.1f" % w[j])
			fp.write(s)	
		if j >= 35 and j < 44:
			s = ("%8.1f" % w[j])
			fp.write(s)
		if j >= 44 and j <= 51:
			s = ("%8.1f" % w[j])
			fp.write(s)
			
		if j == 52: 
			s = ("\t%s" % bin(int(w[j])))
			fp.write(s)	
		if j == 53: 
			s = ("\t0x%05x" % int(w[j]))
			fp.write(s)	
			#print('0b{:020b}'.format(int(w[j])), end='')
			# #print(" ", end='')
			# #print("")
						 
		if j == 54:
			s = ("%11.0f" %  w[j])
			fp.write(s)
		if j == 55:
			s = ("%11.1f" % w[j])
			fp.write(s)
		if j > 55:
			s = ("%10.1f" % w[j])
			fp.write(s)
			
	fp.write("\n\n\n")
	fp.write("1: UDP housekeeping packet frame start\n")
	fp.write("2-13: H-bridge Hall current sensors\n")
	fp.write("19-34: Delta power supplies V, I, V, I ...\n")
	fp.write("36-38: Delta power supplies temperature\n")
	fp.write("39-44: Delta power supplies fan speed\n")
	fp.write("45-47: Heatsink temperatures\n")
	fp.write("49-51: Heatsink fan % PWM control\n")
	fp.write("53: Delta power supplies module on/off status\n")
	fp.write("54: Power converter fault status\n")
	fp.write("55: Power converter Model.Serial Number\n")
	fp.write("56: Controller firmware version\n")
	fp.write("57: Controller firmware loop rate (loops/s)\n")
	fp.write("58: UDP packet counter\n")
	fp.write("59: Controller uptime since reset (s)\n")
	fp.write("60: UDP housekeeping packet frame end\n")
	
	fp.close()
	try:
		os.mkdir(filepath)
	except:
		pass
	print("Writing to file %s" % (filepath+filename))

except KeyboardInterrupt:
   sys.exit()
except Exception as err:
	print(err)
	#sys.exit()
	print("Syncing...")
