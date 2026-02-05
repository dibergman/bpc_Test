import socket 
import sys
import time
#import serial
import numpy as np
#import matplotlib.pyplot as plt
#import struct
#from matplotlib import ticker as tick
import pyvisa


def sds_send(sock, scpi_cmd):
	sock.sendall(scpi_cmd)
	#print(scpi_cmd)
	time.sleep(0.25)
    

F=14
state = sys.argv[1] # off or on


oscope = 'Sig'
td1 = 0.1

remote_ip = "192.168.0.100"
if oscope == "Tek":
	port = 4000 # the port number of the instrument service
if oscope == "Sig": #Siglent
	port = 5025 # the port number of the instrument service

	
try:
	#create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
except socket.error:
	print ("Failed to create socket.")
	sys.exit();
try:
	#Connect to remote server
	s.connect((remote_ip , port))
except socket.error:
	print ("failed to connect to ip " + remote_ip)


#file_str = "maxVI_%s_%s_CH%s.png" %(model, serial, chan)

rm = pyvisa.ResourceManager()
#print(rm.list_resources() )
#inst = rm.open_resource('USB0::1689::851::2347672::0::INSTR')
inst = rm.open_resource('USB0::1689::851::2347693::0::INSTR')
#print(inst.query("*IDN?"))


#AFG1022
#print("Measuring max V and I...")

inst.write('SOUR1:FUNC:SHAP DC')
inst.write('SOUR2:FUNC:SHAP DC')
if state == 'off' or state == 'OFF':
	inst.write('SOUR1:VOLT:LEV:IMM:OFFS 0')
	inst.write('SOUR2:VOLT:LEV:IMM:OFFS 0')
	#inst.write('OUTP1:STAT OFF')
	#inst.write('OUTP2:STAT OFF')
if state == 'on' or state == 'ON':
	inst.write('SOUR1:VOLT:LEV:IMM:OFFS 4.7') # 18 V output
	inst.write('SOUR2:VOLT:LEV:IMM:OFFS 0')
	inst.write('OUTP1:STAT ON')
	inst.write('OUTP2:STAT ON')
	for i in range(11):
		s1 = str(float(i/10*2.08))
		inst.write('SOUR2:VOLT:LEV:IMM:OFFS %s' % s1) # LPE 24 A
		time.sleep(0.2)
		
		
if oscope == 'Sig':
	sds_send(s, b'*RST\n')
	rdg=0
	while (rdg==0):
		try:
			sds_send(s, b'*IDN?\n')
			rdg = s.recv(100)
			print(rdg)
		except:
			pass
			#print(rdg)
	try:		
		rdg = s.recv(100) # clear serial buffer
	except:
		pass
	print("Configuring instruments...")
	sds_send(s, b'C1:TRACE ON\n')
	sds_send(s, b'C2:TRACE OFF\n')
	sds_send(s, b'C3:TRACE OFF\n')
	sds_send(s, b'C4:TRACE ON\n')
	#set Siglent scope trigger
	sds_send(s, b'C1:ATTENUATION 10\n')
	sds_send(s, b'C4:TRIG_LEVEL 0.1\n')          # Trigger level. Divid by atten factor
	sds_send(s, b'TRIG_MODE AUTO\n')            # Auto trigger mode
	sds_send(s, b'C1:VOLT_DIV 10\n')
	sds_send(s, b'C1:COUPLING D1M\n')

s.close()
