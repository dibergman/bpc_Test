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
	fp.write("\n\n\n\n\n\n\nUDP Housekeeping Data for LT-EL-SR-PS-CRR-%s S/N %s\n\n" \
	         % (model, serial) )
	fp.write("Full power data for CH%s\n\n" % chan)         
			
	fp.write('{:25} {:25} {:25} {:25}\n'.format('1. Frame start %d' % w[0], '16. %2.1f' % w[15], \
			'31. Delta PS V %2.1f' % w[30], '46. Heatsink 2 Temp %2.1f' % w[45]) )
			
	fp.write('{:25} {:25} {:25} {:25}\n'.format('2. Hall sensor 1 %2.1f' % w[1], '17. %2.1f' % w[16], \
	'32. Delta PS I %2.1f' % w[31], '47. Heatsink 3 Temp %2.1f' % w[46]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('3. Hall sensor 2 %2.1f' % w[2], '18. %2.1f' % w[17], \
	'33. Delta PS V %2.1f' % w[32], '48. %2.1f' % w[47]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('4. Hall sensor 3 %2.1f' % w[3], '19. Delta PS V %2.1f' % w[18], \
	'34. Delta PS I %2.1f' % w[33], '49. Heatsink fan PWM %2.0f' % w[48]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('5. Hall sensor 4 %2.1f' % w[4], '20. Delta PS I %2.1f' % w[19], \
	'35. %2.1f' % w[34], '50. Heatsink fan PWM %2.0f' % w[49]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('6. Hall sensor 5 %2.1f' % w[5], '21. Delta PS V %2.1f' % w[20], \
	'36. Delta PS1 Temp %2.1f' % w[35], '51. Heatsink fan PWM %2.0f' % w[50]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('7. Hall sensor 6 %2.1f' % w[6], '22. Delta PS I %2.1f' % w[21], \
	'37. Delta PS2 Temp %2.1f' % w[36], '52. %2.1f' % w[51]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('8. Hall sensor 7 %2.1f' % w[7], '23. Delta PS V %2.1f' % w[22], \
	'38. Delta PS3 Temp %d' % w[37], '53. Delta Mod On/Off 0b%s' % "{0:b}".format(int(w[52]) )) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('9. Hall sensor 8 %2.1f' % w[8], '24. Delta PS I %2.1f' % w[23], \
	'39. Delta PS1 Fan1 %2.0f' % w[38], '54. Fault status 0x%05x' % int(w[53])) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('10. Hall sensor 9 %2.1f' % w[9], '25. Delta PS V %2.1f' % w[24], \
	'40. Delta PS1 Fan2 %2.0f' % w[39], '55. Mod.Ser No. %s' % '{:<11.3f}'.format(w[54]/1000) ) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('11. Hall sensor 10 %2.1f' % w[10], '26. Delta PS I %2.1f' % w[25], \
	'41. Delta PS2 Fan1 %2.0f' % w[40], '56. F/W version %2.1f' % w[55]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('12. Hall sensor 11 %2.1f' % w[11], '27. Delta PS V %2.1f' % w[26], \
	'42. Delta PS2 Fan2 %2.0f' % w[41], '57. Loop rate (/s) %2.0f' % w[56]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('13. Hall sensor 12 %2.1f' % w[12], '28. Delta PS I %2.1f' % w[27], \
	'43. Delta PS3 Fan1 %2.0f' % w[42], '58. UDP packet count %2.0f' % w[57]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('14. %2.1f' % w[13], '29. Delta PS V %2.1f' % w[28], \
	'44. Delta PS3 Fan2 %2.0f' % w[43], '59. Uptime (s) %2.0f' % w[58]) )
	
	fp.write('{:25} {:25} {:25} {:25}\n'.format('15. %2.1f' % w[14], '30. Delta PS I %2.1f' % w[29], \
	'45. Heatsink1 Temp %2.1f' % w[44], '60. Frame end %2.0f' % w[59]) )
	
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
