#!/usr/bin/env python
import sys
import socket
import time

shell = "/bin/sh"

def usage(programname):
	print "python connect-back door"
	print "Usage: %s " % programname

def recv_timeout(the_socket, timeout=2):
	the_socket.setblocking(0)
	begin = time.time()
	getsome = False
	buffer = []
	if timeout < 0:
		timeout = 2
	dbl_timeout = timeout * 2

	while 1:
		if getsome and time.time() - begin > timeout:
			break
		elif time.time() - begin > dbl_timeout:
			break

		try:
			data = the_socket.recv(8192)
			if data:
				if not getsome:
					getsome = True
				buffer.append(data)
				begin = time.time()
			else:
				time.sleep(0.1)
		except socket.error, e:
			#print 'cause error', e
			pass
	return ''.join(buffer)


def main():
	if len(sys.argv) !=3:
		usage(sys.argv[0])
		sys.exit(1)

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host = socket.gethostbyname(sys.argv[1])
	port = int(sys.argv[2])
	try:
		print 'connect to %s:%d' % (host, port)
		#s.connect((host, port))
		s.connect(("localhost", 9092)) # proxy
		print "[+]Connect OK."
		s.send("GET /test HTTP/1.1\r\nHost: %s:%d\r\n\r\n" % (host, port))
		print recv_timeout(s)
		s.close()
	except socket.error, e:
		print "[-]Can't connect", e
		s.close()
		sys.exit(2)
	


if __name__ == "__main__":
	main()