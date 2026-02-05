#Energy extraction test
import socket 
import sys
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import struct
from matplotlib import ticker as tick
import pyvisa
import os


def sds_send(sock, scpi_cmd):
	sock.sendall(scpi_cmd)
	print(scpi_cmd)
	time.sleep(0.15)
    

#oscope = "Tek"
oscope = "Sig"

F=14
model = sys.argv[1]
serial = sys.argv[2]
chan = sys.argv[3]

td1=0.1

modelname = "%s_%s" % (model,serial)
filename = "%s_%s_CH%s_energy.png" %(model, serial, chan)
#filepath = './2ch/' + modelname + '/'
filepath = "./_temp/"

rm = pyvisa.ResourceManager()
#print(rm.list_resources() )
inst = rm.open_resource('USB0::1689::851::2347672::0::INSTR')
#inst = rm.open_resource('USB0::1689::851::2347693::0::INSTR')
#print(inst.query("*IDN?"))

remote_ip = "192.168.0.101"
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

def smooth_wfm(wfm):
	N=len(wfm)
	L=16
	w = np.zeros(N-L)
	for i in range(N-L):
		w[i] = np.mean(wfm[i:i+L])
	return w


def get_MSO4054_wfm(CH):
	ch_str = 'DATA:SOU ' + CH + '\n'
	#s.send(b'DATA:SOU CH2\n')
	s.send(ch_str.encode('UTF-8'))
	s.send(b'WFMOutpre:BYT_Nr 2\n')
	s.send(b'CURV?\n')
	time.sleep(1)
	data = s.recv(20100)
	#data = s.recv(200200)
	#print(len(data))
	#print(data[0:20])
	#print(len(data))
	wfm = np.asarray(struct.unpack('9900h', data[0+100:19800+100]))
	#wfm = np.asarray(struct.unpack('9900B', data[0+100:9900+100]))
	#print(len(wfm))
	s.send(b'WFMOutpre:YMU?\n')
	time.sleep(0.3)
	rdg=bytearray()
	while len(rdg)<3:
		tmp = s.recv(100)
		rdg.extend(tmp)
	m = float(rdg.decode("UTF-8"))
	#print(m)
	s.send(b'WFMOutpre:YOF?\n')
	time.sleep(0.3)
	rdg=bytearray()
	while len(rdg)<3:
		tmp = s.recv(100)
		rdg.extend(tmp)
	b = float(rdg.decode("UTF-8"))
	#print(b)
	#print(m)
	wfm1 = (wfm-b)*m
	#wfm1 = wfm*1inst = rm.open_resource('USB0::1689::851::2347693::0::INSTR')
	#print(wfm1[0:50])
	#fig = plt.figure(1, figsize=(14,9))
	#plt.plot(wfm1, 'k.', label = "") # dib
	#plt.show()
	return wfm1
	

def get_MSO4054_XINcr():
	s.send(b'WFMOutpre:XINcr?\n')
	rdg=bytearray()
	while len(rdg)<2:
		tmp = s.recv(4096)
		rdg.extend(tmp)
	#print(rdg)
	Ts = rdg.decode("UTF-8")
	return float(Ts)


def get_SIGLENT_wfm(CH):
    #import struct
    #import numpy as np
    #import time

    s.send(b'CHDR OFF\n') # suppress headers
    
    ch_str = f'C{CH}:WF? DAT2\n'  # Request waveform data from channel CH
    s.send(ch_str.encode('UTF-8'))

    # Receive header
    header1 = s.recv(5)
    header = s.recv(2)
    print("header = %s" % header)
    if header != b'#9':
    #if header != b'C2':
        raise Exception("Unexpected header format")

    # Receive length of waveform data
    len_str = s.recv(9)
    num_bytes = int(len_str.decode())
    print(num_bytes)

    # Receive waveform data
    z = bytearray()
    while len(z) < num_bytes:
        data = s.recv(1024)
        z.extend(data)

    # Convert binary data to numpy array
    wfm = np.frombuffer(z, dtype=np.int8)
    print(len(wfm))

    # Request vertical scale (e.g., V/div)
    s.send(f'C{CH}:VDIV?\n'.encode('UTF-8'))
    vdiv = float(s.recv(100).decode())
    print(vdiv)

    # Request horizontal scale (e.g., s/div)
    s.send(f'TDIV?\n'.encode('UTF-8'))
    tdiv = float(s.recv(100).decode())
    print(tdiv)
    Ts = tdiv*14/num_bytes
    print(Ts)

    # Request vertical offset
    s.send(f'C{CH}:OFST?\n'.encode('UTF-8'))
    ofst = float(s.recv(100).decode().strip())
    print(ofst)

    # Apply vertical scaling
    # Siglent sends data centered around 127 (i.e., 8-bit unsigned int)
    volt_per_bit = vdiv / 25  # 10 div screen, 250 levels
    print(volt_per_bit)
    wfm1 = wfm*volt_per_bit-ofst

    return wfm1, Ts


print("Testing energy extraction...")	

#AFG1022
inst.write('SOUR1:FUNC:SHAP DC')
if model == "6201" or model == "6202":
	inst.write('SOUR1:VOLT:LEV:IMM:OFFS 4.7')
if model == "6101" or model=='6401':
	inst.write('SOUR1:VOLT:LEV:IMM:OFFS 4.8')
inst.write('OUTP1:STAT ON')

#inst.write('SOUR1:FUNC:SHAP SQU')
#inst.write('SOUR1:VOLT:LEV:IMM:OFFS 1')
#inst.write('SOUR1:VOLT:LEV:IMM:AMPL 0.5')
#inst.write('SOUR1:FREQ:FIX 100')
#inst.write('OUTP1:STAT ON')
#print(inst.query('OUTP2:STAT?'))
#print(inst.query('SOUR2:FUNC:SHAP?'))


try:
	
	if oscope == "Tek":
		s.send(b'SELECT:CH1 OFF\n')
		s.send(b'SELECT:CH2 OFF\n')
		s.send(b'SELECT:CH3 ON\n')
		s.send(b'SELECT:CH4 ON\n')
		time.sleep(td1)
		s.send(b'TRIG:A:MOD AUTO\n') # clear the display
		time.sleep(2)
		#set Tek scope trigger
		s.send(b'TRIG:A:EDGE:SOUR CH3\n')
		s.send(b'TRIG:A:LEV -1\n')
		s.send(b'TRIG:A:EDGE:SLO RISE\n')
		s.send(b'TRIG:A:MOD NORM\n')
		#set Tek scope horizontal scale
		s.send(b'HOR:SCA 0.02\n')
		s.send(b'HOR:DEL:MOD ON\n')
		s.send(b'HOR:DEL:TIM 0.06\n')
		s.send(b'HOR:RECOrdlength 10000\n')
		#set Tek scope vertical scale
		s.send(b'CH3:SCALE 5\n')
		s.send(b'CH3:COUP DC\n')
		s.send(b'CH4:SCALE 2\n')
		s.send(b'CH4:COUP DC\n')
		s.send(b'CH3:POS 0\n')
		s.send(b'CH4:POS 0\n')
		s.send(b'CH3:BANDWIDTH TWENTY\n')
		s.send(b'CH4:BANDWIDTH TWENTY\n')
	
	
	if oscope == "Sig":
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
		try:		
			rdg = s.recv(100) # clear serial buffer
		except:
			pass
		print("Configuring instruments...")
		time.sleep(3)
		
		sds_send(s, b'C1:TRA OFF\n')
		sds_send(s, b'C2:TRA OFF\n')
		sds_send(s, b'C3:TRA OFF\n')
		sds_send(s, b'C4:TRA OFF\n')
		
		sds_send(s, b'C3:ATTENUATION 1\r\n')
		sds_send(s, b'C3:COUPLING D1M\r\n')               
		sds_send(s, b'C3:VOLT_DIV 5\r\n')            
		sds_send(s, b'C3:OFFSET 0V\r\n')     
		
		sds_send(s, b'C4:ATTENUATION 1\n')
		sds_send(s, b'C4:COUPLING D1M\n')               
		sds_send(s, b'C4:VOLT_DIV 2\n')            
		sds_send(s, b'C4:OFFSET 0\n')  
		
		sds_send(s, b'BWL C3,ON,C4,ON\n')
		
		sds_send(s, b'TRIG_MODE AUTO\n') # clear the display
		#set Sig scope trigger
		sds_send(s, b'C3:TRIG_LEVEL -1\n')
		sds_send(s, b'TRIG_MODE NORM\n')
		
		#set Sig scope horizontal scale
		sds_send(s, b'TIME_DIV 0.02\n')
		sds_send(s, b'TRIG_DELAY -0.06\n')
		sds_send(s, b'MEMORY_SIZE 7K\n')
		 
		
		
		
			
	
	
	print("Make sure DUT channel is on, verify current, ", end="")
	print("then turn off channel.")
	print("Press Enter when ready.")
	input()
	print("Acquiring data")
	
	time.sleep(2)
	if oscope == "Tek":
		Wfm2 = get_MSO4054_wfm('CH3')
		Wfm3 = get_MSO4054_wfm('CH4')
		Ts = get_MSO4054_XINcr()
	if oscope == "Sig":
		[Wfm2, Ts] = get_SIGLENT_wfm('3')
		[Wfm3, Ts] = get_SIGLENT_wfm('4')

	N = len(Wfm3)
	#print(N)
	t = np.arange(N)*Ts
	f0 = 1/(N*Ts)
	f = np.arange(N)*f0
	
	y1 = smooth_wfm(Wfm2)*1.9
	y2 = smooth_wfm(Wfm3)*5
	M=len(y1)
	
	#fp = open("test.txt", 'a')
	#fp.write("%f,%f,%f,%f,%f,%f\n" %(f, vtrim, itrim, vcoil, pha1, pha2))
	#fp.close()

#except socket.error:
except Exception as err:
	#print ("failed to send to ip " + remote_ip)
	print(err)
	
#s.close()

print("Making plot")
fig1 = plt.figure(1, figsize=(11,8))
#fig1 = plt.figure(1)
ax1a = fig1.add_subplot(1,1,1)
#ax1b = fig1.add_subplot(2,1,2)
		
plt.figure(1)
plt.axes(ax1a)
plt.plot(t[0:M],y1, 'k', label = "Vout") # dib
plt.plot(t[0:M],y2, 'r', label = "DC Bus") # dib
ax1a.set_xlabel('Time (s)', fontsize=F)
ax1a.set_ylabel('Amplitude (V)', fontsize=F)
title_str = "Model %s S/N %s CH %s Energy Extraction" % (model, serial, chan)
plt.title(title_str, fontsize=F)
#ax1.ticklabel_format(useOffset=False, style='plain')
plt.xticks(fontsize=F, rotation=0)
plt.yticks(fontsize=F, rotation=0)
#plt.ylim([-0.01, 0.01])
plt.grid('True')
#plt.text(0.0012,0.075,"Vout = 410 V", fontsize = 14)
plt.legend(loc="lower right", fontsize = 14)
#ax1a.yaxis.set_major_formatter(FormatStrFormatter('%1.5f'))
ax1a.yaxis.set_major_formatter(tick.FormatStrFormatter('%1.4f'))

try:
	os.mkdir(filepath)
except:
	pass
print("Writing to file %s" % (filepath+filename))
plt.savefig(filepath+filename)
plt.show()

inst.write('SOUR1:VOLT:LEV:IMM:OFFS 0')
#inst.write('OUTP1:STAT OFF')


s.close()
