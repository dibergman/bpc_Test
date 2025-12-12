import sys
import subprocess
import os
from os import system
import socket
import numpy as np
import struct
import time


system('clear')
print("")
x='0'
while( x!='1' and x!='2' and x!='3' and x!='4'):
	x = input("Select chassis model: 1) 6201, 2) 6202, 3) 6101, 4) 6401 ")
	if x=='1':
		model = 'BPC-2CH-S-18V-24A'
		model1 = '6201'
		Imax=19
	if x=='2':
		model = 'BPC-2CH-F-18V-24A'
		model1 = '6202'
		Imax=19
	if x=='3':
		model = 'BPC-1CH-S-18V-90A'
		model1 = '6101'
	if x=='4':
		model = 'BPC-4CH-S-18V-10A'
		model1 = '6401'
		Imax=7
	if x!='1' and x!='2' and x!='3' and x!='4':
		print("Please enter 1, 2, 3, or 4.")

if x=='1' or x=='2': 
	chan = [1,2]
if x=='3': 
	chan = [1]
if x=='4': 
	chan = [1,2,3,4]


x='0'
while(len(x)!=4):	
	x = input("Enter serial number: ")
	if(len(x)!=4):
		print("Serial number should be 4 digits.")
serial=x
y=str(int(x))
ip = '192.168.0.' + y

message = b"Loop"
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(2)
	server_address = (ip, 5000)

except Exception as err:
	print("Socket error: %s" % err)



print("")
print("Chassis is %s S/N %s. " % (model, serial), end = "")

x = input("If correct, press 'y' then Enter: ")
if x != 'y':
	sys.exit()
#print(ip)


for k in chan:
	try:
		system('clear')
		print("\nTesting channel %s\n\n" % k)
		time.sleep(2)
		x='r'
		while x=='r':
			system('clear')
			print("\n\n")
			print("1. Testing wideband noise...\n")
			print("a. With BPC CH%s OFF, verify load and differential probe connections." % k) 
			print("b. Connect signal generator cable into CH%s_RegOut connector on bench channel interface board." % k)
			print("c. Turn BPC CH%s ON." % k)
			print("\nPress Enter when ready or 's' to skip...", end="")
			x = input()
			if x=='':
				cmd_str = "sudo python3 /home/dib/noise1.py %s %s %s" % (model1, serial, k)
				os.system(cmd_str)
				print("\nPress Enter to continue or 'r' to redo step...", end="")
				x = input()
			if x!='' and x!='s':
				x='r'

		x='r'
		while x=='r':
			system('clear')
			print("\n\n")
			print("2. Testing step response...\n")
			print("a. Verify load and differential probe connections.")
			print("\nPress Enter when ready or 's' to skip...", end="")   	   
			x=input()
			if x=='':
				cmd_str = "sudo python3 /home/dib/step1.py %s %s %s" % (model1, serial, k)
				os.system(cmd_str)
				print("\nPress Enter to continue or 'r' to redo step...", end="")
				x = input()
			if x!='' and x!='s':
				x='r'
		
		x='r'
		while x =='r':
			system('clear')
			print("\n\n")
			print("3. Testing common mode noise...\n")
			print("a. Move differential probe black clip lead onto DUT chassis point.")	   
			print("\nPress Enter when ready or 's' to skip...", end="")  
			x = input()
			if x=='':
				cmd_str = "sudo python3 /home/dib/noise2.py %s %s %s" % (model1, serial, k) 
				os.system(cmd_str)
				print("\nPress Enter to continue or 'r' to redo step...", end="")
				x = input()
			if x!='' and x!='s':
				x='r'

		
		
		
		x='r'
		while x =='r':
			system('clear')
			print("\n\n")
			print("4. Testing narrowband noise...\n") 
			print("a. Verify load and BNC cable connections.")	   
			print("\nPress Enter when ready or 's' to skip...", end="")   
			x=input()
			if x=='':
				cmd_str = "sudo python3 /home/dib/noise3.py %s %s %s" % (model1, serial, k)
				os.system(cmd_str)
				print("\nPress Enter to continue or 'r' to redo step...", end="")
				x = input()
			if x!='' and x!='s':
				x='r'

		

		x='r'
		while x=='r':
			system('clear')
			print("\n\n")
			print("5. Testing energy extraction...\n") 
			print("a. Verify o'scope2 CH3 and CH4 connections to Nano board CH%s_Vout and CH%s_Spare connectors." % (k, k))
			print("\nPress Enter when ready or 's' to skip...", end="")
			x=input()
			if x=='':
				cmd_str = "sudo python3 /home/dib/energy_extract.py %s %s %s" % (model1, serial, k)
				os.system(cmd_str)
				print("\nPress Enter to continue or 'r' to redo step...", end="")
				x = input()
			if x!='' and x!='s':
				x='r'

		x='r'
		while x=='r':
			system('clear')
			print("\n\n")
			print("6. Testing max V and I...\n")
			print("a. Verify load connection")
			print("\nPress Enter when ready or 's' to skip...", end="")
			x=input()
			flag1=0
			flag2=0
			if x=='':
				print("Measuring max V and I...")
				try:
					sock.sendto(message, server_address)
					data, addr = sock.recvfrom(2048)
				except:
					print("Can't connect to power converter ethernet. Wrong chassis S/N or ethernet cable unplugged......")
					print("\nPress Enter to try again...", end="")
					flag1=1
					x='r'
					input()
				if flag1!=1:
					current = 0
					j=0
					os.system("sudo python3 /home/dib/maxVI.py on")
					while (current < Imax):
						sock.sendto(message, server_address)
						data, addr = sock.recvfrom(2048)
						w = np.asarray(struct.unpack('<60f', data))
						if model1=='6201' or model1=='6202':
							current = (w[(k-1)*4+1]+w[(k-1)*4+2]+w[(k-1)*4+3]+w[(k-1)*4+4])/2
						if model1=='6401':
							current = (w[(k-1)*2+1]+w[(k-1)*2+2])/2
						#print(current)
						time.sleep(0.5)
						j=j+1
						if j >= 12:
							print("Current not at max value. Check connections.")
							print("Press Enter when ready.")
							os.system("sudo python3 /home/dib/maxVI.py off")
							current=100 # break out of while current<21 loop
							flag2=1
							x='r'
							input()
												
				if flag1!=1 and flag2!=1:	
					print("d. Measure output voltage with DMM and output current with clamp. Record V and I in test sheet.")	
					input("e. Wait for heatsink temperature to reach final value, then press Enter.")
					cmd_str = "sudo python3 /home/dib/udp_get_once.py %s %s %s %s" % (ip, model1, serial, k)
					os.system(cmd_str)
					time.sleep(1)
					os.system("sudo python3 /home/dib/maxVI.py off")
					print("\nPress Enter to continue or 'r' to redo step...", end="")
					x = input()
			if x!='' and x!='s':
				x='r'
						
										
		if k==len(chan):
			print("\n")
			print("Test complete! ... ")
			#print("\n")

			filepath="/home/dib/%s/%s_%s/" % (model,model1,serial)
			print("Copy files from /home/dib/_temp/ to %s ? (y/n)" % filepath )
			x=input()
			if x=='y':
				try:
					os.mkdir(filepath)
				except:
					print("Cannot create directory")
				cmd_str = "cp /home/dib/_temp/%s_%s* %s." % (model1, serial, filepath)
				os.system(cmd_str)
				print("\n")
				print("Files copied.")
				cmd_str = "sudo chown dib %s/." % (filepath)
				os.system(cmd_str)
			
	except Exception as err:
		print(err)

