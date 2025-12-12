#Low frequency noise - band limit 10 kHz
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
	#now = time.time()
	#while (time.time()-now)<1:
	#	sock.sendall(b'*OPC\n')
	#	sock.sendall(b'*OPC?\n')
	#	x=sock.recv(1000)
	#	print(x)
	#	if x==b'1\n':
	#		break
	#print()
	time.sleep(0.3)
    

#oscope = "Tek"
oscope = "Sig"

F=14
model = sys.argv[1]
serial = sys.argv[2]
chan = sys.argv[3]

modelname = "%s_%s" % (model,serial)
filename = "%s_%s_CH%s_lf_noise.png" %(model, serial, chan)
#filepath = './2ch/' + modelname + '/'
filepath = "./_temp/"

td=0.3
td1=0.1

def get_MSO4054_wfm(CH):
	ch_str = 'DATA:SOU ' + CH + '\n'
	#s.send(b'DATA:SOU CH2\n')
	s.send(ch_str.encode('UTF-8'))
	s.send(b'WFMOutpre:BYT_Nr 1\n')
	s.send(b'DATa:STARt 0\n')
	s.send(b'DATa:STOP 100000\n')
	s.send(b'CURV?\n')
	#time.sleep(0.3)
	#data = s.recv(20100)
	#data = s.recv(200200)
	z = bytearray()
	while len(z) < 100000:
		data = s.recv(1000)
		z.extend(data)
	#print(len(z))
	#print(data[0:20])
	#print(len(data))
	#wfm = np.asarray(struct.unpack('9900H', data[0+100:19800+100]))
	#wfm = np.asarray(struct.unpack('99000H', data[0+100:198000+100]))
	wfm = np.asarray(struct.unpack('100000b', z[8:100008]))
	#print(len(wfm))
	time.sleep(td)
	s.send(b'WFMOutpre:YMU?\n')
	rdg=bytearray()
	while len(rdg)<3:
		tmp = s.recv(100)
		rdg.extend(tmp)
	m = float(rdg.decode("UTF-8"))
	time.sleep(td)
	s.send(b'WFMOutpre:YOF?\n')
	rdg=bytearray()
	while len(rdg)<3:
		tmp = s.recv(100)
		rdg.extend(tmp)
	b = float(rdg.decode("UTF-8"))
	#print(b)
	#print(m)
	wfm1 = (wfm-b)*m
	#wfm1 = wfm*1
	#print(wfm1[0:50])
	#fig = plt.figure(1, figsize=(14,9))
	#plt.plot(wfm1, 'k.', label = "") # dib
	#plt.show()
	return wfm1
	

def get_MSO4054_XINcr():
	s.send(b'WFMOutpre:XINcr?\n')
	rdg=bytearray()
	while len(rdg)<3:
		tmp = s.recv(4096)
		rdg.extend(tmp)
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
    print("Waveform length %d" % len(wfm))

    # Request vertical scale (e.g., V/div)
    s.send(f'C{CH}:VDIV?\n'.encode('UTF-8'))
    vdiv = float(s.recv(100).decode())
    print("V/div %f" % vdiv)

    # Request horizontal scale (e.g., s/div)
    s.send(f'TDIV?\n'.encode('UTF-8'))
    tdiv = float(s.recv(100).decode())
    print("t/div %f" % tdiv)
    Ts = tdiv*14/num_bytes
    print("Ts %f" % Ts)

    # Request vertical offset
    s.send(f'C{CH}:OFST?\n'.encode('UTF-8'))
    ofst = float(s.recv(100).decode().strip())
    print("Offset %f " % ofst)

    # Apply vertical scaling
    # Siglent sends data centered around 127 (i.e., 8-bit unsigned int)
    volt_per_bit = vdiv / 25  # 10 div screen, 250 levels
    print("Volt/bit %f" % volt_per_bit)
    wfm1 = wfm*volt_per_bit-ofst

    return wfm1, Ts



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
	
try:
	print("Measuring narrowband noise...")
	print("Configuring instruments...")
	#AFG1022
	inst.write('SOUR1:FUNC:SHAP DC')
	inst.write('SOUR1:VOLT:LEV:IMM:OFFS 0.8') # 5 A into 0.5 ohm load
	if model=='6401':
			inst.write('SOUR1:VOLT:LEV:IMM:OFFS 2.5')
	inst.write('OUTP1:STAT ON')
	
	inst.write('SOUR2:FUNC:SHAP DC')
	inst.write('SOUR2:VOLT:LEV:IMM:OFFS 1.3')
	inst.write('OUTP2:STAT ON')
	
	if oscope == "Tek":
		s.send(b'SELECT:CH1 OFF\n')
		s.send(b'SELECT:CH2 ON\n')
		s.send(b'SELECT:CH3 OFF\n')
		s.send(b'SELECT:CH4 OFF\n')
		#set Tek scope trigger	
		s.send(b'TRIG:A:EDGE:SOUR CH1\n')
		s.send(b'TRIG:A:EDGE:LEV 1\n')
		s.send(b'TRIG:A:MOD AUTO\n')
		#set Tek scope horizontal scale
		s.send(b'HOR:SCA 0.1\n')
		#s.send(b'ACQuire:MODE AVErage\n')
		s.send(b'HOR:RECOrdlength 100000\n')
		#set Tek scope vertical scale
		s.send(b'CH2:SCALE 0.002\n')
		s.send(b'CH2:COUP AC\n')
		s.send(b'CH2:POS 0\n') #position is in divisions
		s.send(b'CH2:BANDWIDTH TWENTY\n')
			
		s.send(b'MEASU:MEAS1:TYPE RMS\n')
		s.send(b'MEASU:MEAS1:SOUR CH2\n')
		s.send(b'MEASU:MEAS1:STATE ON\n')
		
		
	if oscope == "Sig": #Siglent
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
		sds_send(s, b'C1:TRA ON\n') #Trace on/off
		sds_send(s, b'C2:TRA OFF\n')
		sds_send(s, b'C3:TRA OFF\n')
		sds_send(s, b'C4:TRA OFF\n')
				
		sds_send(s, b'C1:TRLV 920e-6\n')          # Trigger level
		sds_send(s, b'TRMD AUTO\n')            # Auto trigger mode
		
		sds_send(s, b'TDIV 100MS\n')                 # Time/div in seconds
		sds_send(s, b'MSIZ 140K\n')                # Memory depth (record length)
		
		sds_send(s, b'C1:VDIV 0.005\n')            # Volts/div
		sds_send(s, b'C1:CPL A1M\n')               # Coupling AC 1MOhm
		sds_send(s, b'C1:OFST 0\n')                # Offset in volts
		sds_send(s, b'C1:BWL ON\n')               # Bandwidth limit: 20 MHz
		sds_send(s, b'C1:ATTN 1\n')
		
		sds_send(s, b'PACU:STDEV,C1\n')
			
	
	print("Acquiring data...")	
	time.sleep(5)
	
	if oscope == "Tek":
		Wfm1 = get_MSO4054_wfm('CH1')
		Ts = get_MSO4054_XINcr()
	if oscope == "Sig":
		[Wfm1a, Ts] = get_SIGLENT_wfm('1')
		Wfm1 = Wfm1a[0:100000]
		
		
	N = len(Wfm1)
	print("N = %d " % N)
	t = np.arange(N)*Ts
	f0 = 1/(N*Ts)
	print("f0 %f" % f0)
	f = np.arange(N)*f0
	
	y = Wfm1
	Y1 = np.fft.fft(y)
	magY1 = abs(Y1)/(N/2)
	
	time.sleep(1)
	if oscope == "Tek":
		s.send(b'MEASU:MEAS1:VAL?\n')
		time.sleep(0.2)
		rdg = s.recv(4096).decode('UTF-8') #convert byte array to list of strings
		rms = np.array(rdg).astype(float) # make list into array then float
		print("RMS noise = %1.6f V" % rms)
	if oscope == "Sig":
		s.sendall(b'C1:PAVA? STDEV\n')       # Query RMS value
		rdg = s.recv(100).decode().strip()
		rms = float(rdg.split(",")[1])
		print("RMS Value:", rms)

	#fp = open("test.txt", 'a')
	#fp.write("%f,%f,%f,%f,%f,%f\n" %(f, vtrim, itrim, vcoil, pha1, pha2))
	#fp.close()

#except socket.error:
except Exception as err:
	#print ("failed to send to ip " + remote_ip)
	print(err)
	
#s.close()

print("Making plot...")
fig1 = plt.figure(1, figsize=(11,8))
#fig1 = plt.figure(1)
ax1a = fig1.add_subplot(2,1,1)
ax1b = fig1.add_subplot(2,1,2)
		
plt.figure(1)
plt.axes(ax1a)
plt.plot(t[5:10000],y[5:10000], 'k', label = "") # dib
ax1a.set_xlabel('Time (s)', fontsize=F)
ax1a.set_ylabel('Output (V)', fontsize=F)
if model=='6101':
	title_str = "Model %s S/N %s CH %s Low Frequency Noise (Iout = 15 A)" \
	% (model, serial, chan)
else:
	title_str = "Model %s S/N %s CH %s Low Frequency Noise (Iout = 5 A)" \
	% (model, serial, chan)
plt.title(title_str, fontsize=F)
#ax1.ticklabel_format(useOffset=False, style='plain')
plt.xticks(fontsize=F, rotation=0)
plt.yticks(fontsize=F, rotation=0)
plt.ylim([-0.01, 0.01])
plt.grid('True')
#plt.text(0.0012,0.075,"Vout = 410 V", fontsize = 14)
#plt.legend(loc="lower left")
#ax1a.yaxis.set_major_formatter(FormatStrFormatter('%1.5f'))
ax1a.yaxis.set_major_formatter(tick.FormatStrFormatter('%1.3f'))
ax1a.xaxis.set_major_formatter(tick.FormatStrFormatter('%1.3f'))
plt.text(0.006, -0.008, "RMS noise = %1.6f V" % rms, fontsize = 14)

#ax1 = fig1.add_subplot(2,1,2)
plt.axes(ax1b)
plt.semilogx(f[1:int(N/2)],magY1[1:int(N/2)], '.-k', label = "") # dib
plt.xlabel('Frequency (Hz)', fontsize=F)
ax1b.set_ylabel('Magnitude (V)', fontsize=F)
#plt.title(title, fontsize=F)
#ax1.ticklabel_format(useOffset=False, style='plain')
plt.xticks(fontsize=F, rotation=0)
plt.yticks(fontsize=F, rotation=0)
plt.ylim([-0.0001, 0.0008])
#plt.ylim([H[N-1]*0.8,H[0]*1.1])
plt.grid('True')
#plt.text(0.0012,0.075,"Vout = 410 V", fontsize = 14)
#plt.legend(loc="lower left")
ax1b.yaxis.set_major_formatter(tick.FormatStrFormatter('%1.6f'))

#plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

try:
	os.mkdir(filepath)
except:
	pass
print("Writing to file %s" % (filepath+filename))
plt.savefig(filepath+filename)
plt.show()

s.close()


