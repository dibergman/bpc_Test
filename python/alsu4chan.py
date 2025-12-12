#python3 program to send serial messages to Arduino Nano to control
#digital IO for on/off/resert control of ALS-U bipolar power converter

import serial
import sys
import time

ser_port = sys.argv[1]

ser = serial.Serial(ser_port, 115200, timeout=10)


Ch1 = 'OFF'
Ch2 = 'OFF'
Ch3 = 'OFF'
Ch4 = 'OFF'
DirectInh1 = 'Inhibited'
DirectInh2 = 'Inhibited'
DirectInh3 = 'Inhibited'
DirectInh4 = 'Inhibited'

while True:
	try:
		print("\n")
		print('{0:30}{1:30}{2:10}'.format("1. Ch1 On", "5. Ch 1 Off", "(On1 DO2)") )		
		print('{0:30}{1:30}{2:10}'.format("2. Ch2 On", "6. Ch 2 Off", "(On1 DO3)") )
		print('{0:30}{1:30}{2:10}'.format("3. Ch3 On", "7. Ch 3 Off", "(On1 DO4)") )
		print('{0:30}{1:30}{2:10}'.format("4. Ch4 On", "8. Ch 4 Off", "(On1 DO5)") )
		print("")
		print('{0:30}{1:30}{2:10}'.format("9. Ch1 PSC Direct Enable", "13. Ch1 PSC Direct Inhibit", "(On2 DO6)") )
		print('{0:30}{1:30}{2:10}'.format("10. Ch2 PSC Direct Enable", "14. Ch2 PSC Direct Inhibit", "(On2 DO7)") )
		print('{0:30}{1:30}{2:10}'.format("11. Ch3 PSC Direct Enable", "15. Ch3 PSC Direct Inhibit", "(On2 DO8)") )
		print('{0:30}{1:30}{2:10}'.format("12. Ch4 PSC Direct Enable", "16. Ch4 PSC Direct Inhibit", "(On2 DO9)") )	
		print("")
		print('{0:60}{1:10}'.format("17. Ch1 Reset", "(Reset DO10)") )
		print('{0:60}{1:10}'.format("18. Ch2 Reset", "(Reset DO11)") )
		print('{0:60}{1:10}'.format("19. Ch3 Reset", "(Reset DO12)") )
		print('{0:60}{1:10}'.format("20. Ch4 Reset", "(Reset DO13)") )
		print("")

		print("Ch1 = %s, %s" % (DirectInh1, Ch1 ) )
		print("Ch2 = %s, %s" % (DirectInh2, Ch2 ) )
		print("Ch3 = %s, %s" % (DirectInh3, Ch3 ) )
		print("Ch4 = %s, %s" % (DirectInh4, Ch4 ) )
		
		print("")

		x = input("Enter Command: ")
		#ser.write(x.encode('utf-8'))
		if x == '1':
			Ch1 = 'ON'
			for i in range(4):
				ser.write(b'01')
				time.sleep(0.05)
		if x == '2':
			Ch2 = 'ON'
			for i in range(4):
				ser.write(b'02')
				time.sleep(0.05)
		if x == '3':
			Ch3 = 'ON'
			for i in range(4):
				ser.write(b'03')
				time.sleep(0.05)
		if x == '4':
			Ch4 = 'ON'
			for i in range(4):
				ser.write(b'04')
				time.sleep(0.05)
		if x == '5':
			Ch1 = 'OFF'
			for i in range(4):
				ser.write(b'05')
				time.sleep(0.05)
		if x == '6':
			Ch2 = 'OFF'
			for i in range(4):
				ser.write(b'06')
				time.sleep(0.05)
		if x == '7':
			Ch3 = 'OFF'
			for i in range(4):
				ser.write(b'07')
				time.sleep(0.05)
		if x == '8':
			Ch4 = 'OFF'
			for i in range(4):
				ser.write(b'08')
				time.sleep(0.05)
		if x == '9':
			for i in range(4):
				DirectInh1 = 'Enabled'
				ser.write(b'09')
				time.sleep(0.05)
		if x == '10':
			DirectInh2 = 'Enabled'
			for i in range(4):
				ser.write(b'10')
				time.sleep(0.05)
		if x == '11':
			DirectInh3 = 'Enabled'
			for i in range(4):
				ser.write(b'11')
				time.sleep(0.05)
		if x == '12':
			DirectInh4 = 'Enabled'
			for i in range(4):
				ser.write(b'12')
				time.sleep(0.05)
		if x == '13':
			DirectInh1 = 'Inhibited'
			for i in range(4):
				ser.write(b'13')
				time.sleep(0.05)
		if x == '14':
			DirectInh2 = 'Inhibited'
			for i in range(4):
				ser.write(b'14')
				time.sleep(0.05)
		if x == '15':
			DirectInh3 = 'Inhibited'
			for i in range(4):
				ser.write(b'15')
				time.sleep(0.05)
		if x == '16':
			DirectInh4 = 'Inhibited'
			for i in range(4):
				ser.write(b'16')
				time.sleep(0.05)
		if x == '17':
			ser.write(b'17')
		if x == '18':
			ser.write(b'18')
		if x == '19':
			ser.write(b'19')
		if x == '20':
			ser.write(b'20')
		
		#print("Command = %s" % x)
			



	except KeyboardInterrupt:
		ser.close()
		quit()
	except Exception as err:
		print(err)
