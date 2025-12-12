#import matplotlib.pyplot as plt
import socket
import time
import numpy as np
import struct
import sys
from os import system

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib

toaddrs = ["dbergman@bnl.gov"]
fromaddr = "bnldrive1@gmail.com"
msg = MIMEMultipart()
msg['Subject'] = 'Bipolar Power Converter Arduino Reset in Cage'
msg['From'] = "dbergman@bnl.gov"      
msg['To'] = ", ".join(toaddrs)

#message "Loop" needed to get data from server
message = b"Loop"
np.set_printoptions(precision=3, suppress = True)

IP = sys.argv[1]
reset_count = 0
fltstat=[0, 0]

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(3)
	# controller test board 192.18.0.6
	# chassis S/N 002 192.168.0.7
	# chassis S/N 004 192.168.0.8
	server_address = (IP, 5000)
	#sock.bind (server_address)
except Exception as err:
	print("Socket error: %s" % err)

td = 0.3
clk = 0

while True:
	try:
		if time.time() - clk >= td:
			fltstat[0]=fltstat[1]
			#print("Sending Loop message %s " % i)
			sock.sendto(message, server_address)
			#Arduino won't send data unless it receives 'Loop' message,
			#but recvfrom() is blocking, so it's possible to get stuck
			#at recvfrom().
			data, addr = sock.recvfrom(2048)
			#print(data)
			#print(len(data))
				
			#y = data.decode("UTF-8") # convert byte array to list of strings
			#z = y.split(',') # separate list of strings by delimiter
			#print(len(z))
			#w = np.array(z[0:86]).astype(np.float) # make list into array then float
			#w = np.array(z).astype(np.float) # make list into array then float
			#w=w/100.0
			w = np.asarray(struct.unpack('<60f', data))
			#system('cls')
			system('clear')
			print('{:25} {:25} {:30} {:30}'.format('1. Frame start %d' % w[0], '16. %2.1f' % w[15], \
			'31. Delta PS V %2.1f' % w[30], '46. Heatsink 2 Temp %2.1f' % w[45]) )
			
			print('{:25} {:25} {:30} {:30}'.format('2. Hall sensor 1 %2.1f' % w[1], '17. %2.1f' % w[16], \
			'32. Delta PS I %2.1f' % w[31], '47. Heatsink 3 Temp %2.1f' % w[46]) )
			
			print('{:25} {:25} {:30} {:30}'.format('3. Hall sensor 2 %2.1f' % w[2], '18. %2.1f' % w[17], \
			'33. Delta PS V %2.1f' % w[32], '48. %2.1f' % w[47]) )
			
			print('{:25} {:25} {:30} {:30}'.format('4. Hall sensor 3 %2.1f' % w[3], '19. Delta PS V %2.1f' % w[18], \
			'34. Delta PS I %2.1f' % w[33], '49. Heatsink fan PWM %2.0f' % w[48]) )
			
			print('{:25} {:25} {:30} {:30}'.format('5. Hall sensor 4 %2.1f' % w[4], '20. Delta PS I %2.1f' % w[19], \
			'35. %2.1f' % w[34], '50. Heatsink fan PWM %2.0f' % w[49]) )
			
			print('{:25} {:25} {:30} {:30}'.format('6. Hall sensor 5 %2.1f' % w[5], '21. Delta PS V %2.1f' % w[20], \
			'36. Delta PS1 Temp %2.1f' % w[35], '51. Heatsink fan PWM %2.0f' % w[50]) )
			
			print('{:25} {:25} {:30} {:30}'.format('7. Hall sensor 6 %2.1f' % w[6], '22. Delta PS I %2.1f' % w[21], \
			'37. Delta PS2 Temp %2.1f' % w[36], '52. %2.1f' % w[51]) )
			
			print('{:25} {:25} {:30} {:30}'.format('8. Hall sensor 7 %2.1f' % w[7], '23. Delta PS V %2.1f' % w[22], \
			'38. Delta PS3 Temp %d' % w[37], '53. Delta PS Mod On/Off Status 0b%s' % "{0:b}".format(int(w[52]) )) )
			
			print('{:25} {:25} {:30} {:30}'.format('9. Hall sensor 8 %2.1f' % w[8], '24. Delta PS I %2.1f' % w[23], \
			'39. Delta PS1 Fan1 %2.0f' % w[38], '54. Fault status 0x%05x' % int(w[53])) )
			
			print('{:25} {:25} {:30} {:30}'.format('10. Hall sensor 9 %2.1f' % w[9], '25. Delta PS V %2.1f' % w[24], \
			'40. Delta PS1 Fan2 %2.0f' % w[39], '55. Model.Serial No. %s' % '{:<10.0f}'.format(w[54]) ) )
			
			print('{:25} {:25} {:30} {:30}'.format('11. Hall sensor 10 %2.1f' % w[10], '26. Delta PS I %2.1f' % w[25], \
			'41. Delta PS2 Fan1 %2.0f' % w[40], '56. Firmware version %2.1f' % w[55]) )
			
			print('{:25} {:25} {:30} {:30}'.format('12. Hall sensor 11 %2.1f' % w[11], '27. Delta PS V %2.1f' % w[26], \
			'42. Delta PS2 Fan2 %2.0f' % w[41], '57. Loop rate (loops/s) %2.1f' % w[56]) )
			
			print('{:25} {:25} {:30} {:30}'.format('13. Hall sensor 12 %2.1f' % w[12], '28. Delta PS I %2.1f' % w[27], \
			'43. Delta PS3 Fan1 %2.0f' % w[42], '58. UDP packet counter %2.0f' % w[57]) )
			
			print('{:25} {:25} {:30} {:30}'.format('14. %2.1f' % w[13], '29. Delta PS V %2.1f' % w[28], \
			'44. Delta PS3 Fan2 %2.0f' % w[43], '59. Uptime since reset %2.0f' % w[58]) )
			
			print('{:25} {:25} {:30} {:30}'.format('15. %2.1f' % w[14], '30. Delta PS I %2.1f' % w[29], \
			'45. Heatsink1 Temp %2.1f' % w[44], '60. Frame end %2.0f' % w[59]) )
			

			clk = time.time()

	except KeyboardInterrupt:
	   sys.exit()
	except Exception as err:
		print(err)
		#sys.exit()
		print("Waiting for connection...")
