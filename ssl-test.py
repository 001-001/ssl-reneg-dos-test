#!/usr/bin/env python

import os
import sys
import socket
import subprocess

arguments = len(sys.argv)

if arguments < 3:
	print("Please use ssl-test.py host port")
	quit()

if str.isdigit(sys.argv[2]) is False:
	print("Incorrect port spcification")
	quit()

target = sys.argv[1]
port = sys.argv[2]
victim = ("a", "b", "c", "d", "e")


def getvictim():
	global victim
	try:
		victim = socket.getaddrinfo(str(target), port, 0, socket.SOCK_STREAM)
	except:
		print("Unable to get address info for " + target)
		quit()

def doscheck():
	dostest = subprocess.Popen(["openssl", "s_client", "-connect", x+":"+y], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	dostest.stdin.write(b"RENEG")
	try:
		print(spacer+"Testing renegotiation")
		output = str(dostest.communicate(timeout=10))
		if "RENEGOTIATING" in output:
			print(spacer + "Renegotiating")
			if "failure" in output:
				print(spacer + "Error in renegotiation\n"+spacer+"Probably not vulnerable to SSL Renegotiation DoS")
				return
			else:
				print(spacer + "No errors in renegotiation\n"+spacer+"Most likely vulnerable to SSL Renegotiation DoS")
				#print(output)
				return
	except:
		print(spacer+"Timeout whilst Renegotiating, most likely not vulnerable")
		quit()

getvictim()

print("Connecting to " + target)
for a, b, c, d, e in victim:
	x = str((e[0]))
	y = str((e[1]))
	spacer = "   " + (len(x)*" ")
	test = subprocess.Popen(["openssl", "s_client", "-connect", x+":"+y], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output = str(test.communicate())
	#print(output)
	if 'Secure Renegotiation IS NOT supported' in output:
		print(x + " - Secure Renegotiation IS NOT supported")
		doscheck()
	#add check anyway thing here
	if 'Secure Renegotiation IS supported' in output:
		print(x + " - Secure Renegotiation IS supported")
		print(spacer + "Checking for Client RENEG")
		doscheck()
	if 'Connection refused' in output:
		print(spacer + "Connection refused")

quit()
