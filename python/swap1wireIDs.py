# Update lines 1, 2, or 7 of SD card.
# Usage - python3 pushSDdib.py IP
import socket
import time
import sys

try:
	IP = sys.argv[1]
except:
	print("Useage - pushSDdib.py IP")

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(3)
	server_address = (IP, 5000)
except Exception as err:
	print("Socket error: %s" % err)


# get data from SD card
#print()
#print("Pulling data from SD card...")
#print()
sock.sendto(b"SDrd", server_address)
data, addr = sock.recvfrom(2048)
data_str = data.decode('UTF-8')
#print(data_str)

#split lines into list
lines = data_str.split('\n')
#print(len(lines))
a = lines[2].split(':', 1)[0] # before colon
b = lines[2].split(':', 1)[1] # after colon
c = lines[3].split(':', 1)[0] # before colon
d = lines[3].split(':', 1)[1] # after colon
lines[2]= a + ":" + d
lines[3]= c + ":" + b


#join the lines back into single string
updated_str = '\n'.join(lines)

print("")
print("Wrote...", end="")
print()
print(updated_str, end="")
sock.sendto(b"SDwr", server_address)
sock.sendto(updated_str.encode('UTF-8'), server_address)
print("...to SD card")
print()
print("Power cycle bipolar power converter for SD card changes to take effect.")
