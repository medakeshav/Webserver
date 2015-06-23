#perf2.py
#request/sec of long running request

#from socket import *
import time
import urllib
#import urllib2
#import requests
from threading import Thread
#import subprocess


#sock = socket(AF_INET, SOCK_STREAM)
#sock.connect(('localhost',8080))
url = 'http://localhost:8080'

n = 0
def monitor():
	global n
	while True:
		time.sleep(1)
		if n != 0:
			print n, 'reqs/sec' ,  round(float(1)/int(n),10), 'time/req'
		n = 0
Thread(target=monitor).start()
while True:
	urllib.urlopen(url)
	#urllib2.urlopen(url).read()
	#sock.send('GET /')
	#sock.recv(100)
	n += 1

