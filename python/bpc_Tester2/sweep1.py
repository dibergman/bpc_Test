# slow triangle setpoint when measuring bridge outputs
import socket 
import sys
import time
import serial
import numpy as np
#import matplotlib.pyplot as plt
#import struct
#from matplotlib import ticker as tick
import pyvisa


def sds_send(sock, scpi_cmd):
    sock.sendall(scpi_cmd)
    print(scpi_cmd)
    time.sleep(0.5)
    

oscope = 'Sig'
td1=0.1
F=14

#file_str = "step_resp_%s_%s_CH%s.png" %(model, serial, chan)

rm = pyvisa.ResourceManager()
#print(rm.list_resources() )
#inst = rm.open_resource('USB0::1689::851::2347672::0::INSTR')
inst = rm.open_resource('USB0::1689::851::2347693::0::INSTR')
#print(inst.query("*IDN?"))

remote_ip = "192.168.0.100"
#port = 4000 # the port number of the instrument service
port = 5025
	
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


#AFG1022
#inst.write('SOUR1:FUNC:SHAP DC')
#inst.write('SOUR1:VOLT:LEV:IMM:OFFS 2.1')

inst.write('SOUR1:FUNC:SHAP RAMP')
inst.write('SOUR1:VOLT:LEV:IMM:OFFS 0')
inst.write('SOUR1:VOLT:LEV:IMM:AMPL 4')
inst.write('SOUR1:FREQ:FIX 0.125')
inst.write('OUTP1:STAT ON')
#print(inst.query('OUTP2:STAT?'))
#print(inst.query('SOUR2:FUNC:SHAP?'))


try:
	#print("Acquiring data")
	if oscope == 'Tek':
		s.send(b'SELECT:CH1 ON\n')
		s.send(b'SELECT:CH2 ON\n')
		s.send(b'SELECT:CH3 OFF\n')
		s.send(b'SELECT:CH4 ON\n')
		#set Tek scope trigger
		s.send(b'TRIG:A:EDGE:SOUR CH1\n')
		s.send(b'TRIG:A:LEV 1\n')
		s.send(b'TRIG:A:EDGE:SLO RISE\n')
		#set Tek scope horizontal scale
		s.send(b'HOR:SCA 800e-9\n')
		s.send(b'HOR:DEL:MOD ON\n')
		s.send(b'HOR:DEL:TIM 0\n')
		#set Tek scope vertical scale
		s.send(b'CH1:SCALE 10\n')
		s.send(b'CH1:COUP DC\n')
		s.send(b'CH1:POS 0\n')
		s.send(b'CH2:SCALE 10\n')
		s.send(b'CH2:COUP DC\n')
		s.send(b'CH2:POS 0\n')
	if oscope == 'Sig':
		sds_send(s, b'*RST\n')
		rdg=0
		x=0
		while (rdg==0 and x<10):
			try:
				sds_send(s, b'*IDN?\n')
				rdg = s.recv(1000)
				print(rdg)
			except:
				x+=1
				#print(rdg)
		#try:		
		#	rdg = s.recv(100) # clear serial buffer
		#except:
		#	pass
		print("Configuring instruments...")
		time.sleep(3)
		sds_send(s, b'C1:TRA OFF\n')
		sds_send(s, b'C2:TRA OFF\n')
		sds_send(s, b'C3:TRA OFF\n')
		sds_send(s, b'C4:TRA OFF\n')
		#set Siglent scope trigger
		sds_send(s, b'C1:TRLV 0.3\n')          # Trigger level
		sds_send(s, b'TRMD AUTO\n')            # Auto trigger mode
				
		#set Siglent scope horizontal scale
		sds_send(s, b'MSIZ 14K\n')                # Memory depth (record length)
		sds_send(s, b'TDIV 500e-9\n')                 # Time/div in seconds
		sds_send(s, b'TRDL 0\n')
		
		#set Siglent scope vertical scale
		sds_send(s, b'C1:ATTENUATION 10\n')
		sds_send(s, b'C1:COUPLING D1M\n')
		sds_send(s, b'C1:VOLT_DIV 5\n')
		sds_send(s, b'C1:OFFSET 0\n')
		
		sds_send(s, b'C2:ATTENUATION 10\n')
		sds_send(s, b'C2:COUPLING D1M\n')
		sds_send(s, b'C2:VOLT_DIV 5\n')
		sds_send(s, b'C2:OFFSET 0\n')
		
		#sds_send(s, b'CH1:POS -4\n') #position is in divisions
		sds_send(s, b'C4:ATTENUATION 1\n')
		sds_send(s, b'C4:COUPLING D1M\n')
		sds_send(s, b'C4:VOLT_DIV 5\n')
		sds_send(s, b'C4:OFFSET -10\n')
		#sds_send(s, b'CH4:POS -4\n')
		
		sds_send(s, b'BWL C1,ON,C2,ON,C4,ON\n')
			
	#wait 10 s then turn function generator outputs off
	clk = time.time()
	while time.time()-clk < 15:
		print("Stopping in %d seconds...\r" % (clk+15-time.time()+1), end="")
		time.sleep(1)
	inst.write('SOUR1:FUNC:SHAP DC')
	inst.write('SOUR1:VOLT:LEV:IMM:OFFS 0')
	inst.write('OUTP1:STAT OFF')
	inst.write('SOUR2:FUNC:SHAP DC')
	inst.write('SOUR2:VOLT:LEV:IMM:OFFS 0')
	inst.write('OUTP2:STAT OFF')
	print("")

except Exception as err:
	#print ("failed to send to ip " + remote_ip)
	print(err)
	
s.close()

