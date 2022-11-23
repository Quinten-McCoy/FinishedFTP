#Client side file transfer using TLS to Server
#Create a socket for TCP packets to IPV4 addresses and wrap in TLS context.
#Load Root certificate to verify server Certificate is authentic
#Once connection is establised send file data until entirely sent then close connection.
import socket, ssl, sys

HOST = '172.24.109.142'
PORT = 555
ADDR = (HOST, PORT)
HEADER = 1024

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#Do not check host name matches since cert does not match domain name
context.check_hostname = False


#SSL version 2, 3 are insecure so they have been blocked
context.options |= ssl.OP_NO_SSLv2
context.options |= ssl.OP_NO_SSLv3

def server_connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Finding server and connecting
	print(f"[CLIENT] Finding server on {ADDR}")	
	s.connect(ADDR)
	print(f'[CLIENT] Found server on {ADDR}')

	secureS = context.wrap_socket(s, server_side= False)
	print(f'[CLIENT] Secure Connection Established')

	cn = input('Enter username: ')
	password = input('Enter password: ')

	#Sending login info to server
	msg = (f'{cn}<SEPERATOR>{password}').encode()
	secureS.send(msg)

	selection = input('1: Send File\n2: Down File\n3: Exit\n')

	if selection == '1':
		send_file(secureS)
	elif selection == '2':
		pass
	else:
		print('[CLIENT] Closing Program')
		sys.exit()

def send_file(secureS): 
	print(f'[CLIENT] Sending File: transfer.txt')
	with open('transfer.txt', 'rb') as f:
		data = f.readlines()
	data_byt = str(data).encode()
	secureS.sendall(data_byt)
	secureS.shutdown(1)
	secureS.close()
	print('[CLIENT] File sent, closing program')
	sys.exit()


server_connect()