# 50.012 network lab 1

from socket import *
import sys, os
import _thread as thread

proxy_port=8079
proxy_ip = "localhost"
cache_directory = "./cache/"

def client_thread(clientFacingSocket):
	
	clientFacingSocket.settimeout(5.0)

	try:
		message = clientFacingSocket.recv(4096).decode()
		msgElements = message.split()
		
		if len(msgElements) < 5 or msgElements[0].upper() != 'GET' or 'Range:' in msgElements:
			# print("non-supported request: " , msgElements)
			clientFacingSocket.close()
			return

		# Extract the following info from the received message
		#   webServer: the web server's host name
		#   resource: the web resource requested
		#   file_to_use: a valid file name to cache the requested resource
		#   Assume the HTTP request is in the format of:
		#      GET http://www.mit.edu/ HTTP/1.1\r\n
		#      Host: www.mit.edu\r\n
		#      User-Agent: .....
		#      Accept:  ......

		resource = msgElements[1].replace("http://","", 1)
	
		hostHeaderIndex = msgElements.index('Host:')
		webServer = msgElements[hostHeaderIndex+1]

		port = 80

		print("webServer:", webServer)
		print("resource:", resource)

		message=message.replace("Connection: keep-alive","Connection: close")
		
		website_directory = cache_directory + webServer.replace("/",".") + "/"

		if not os.path.exists(website_directory):
			os.makedirs(website_directory)
		
		file_to_use = website_directory + resource.replace("/",".")

	except:
		print(str(sys.exc_info()[0]))                                                
		clientFacingSocket.close()
		return
		
	# Check whether the file exists in the cache
	try:
		with open(file_to_use, "rb") as f:
			# ProxyServer finds a cache hit and generates a response message
			print("served from the cache")
			while True:
				buff = f.read(4096)
				if buff:
					# Fill in start
					clientFacingSocket.send(buff)
					# Fill in end
				else:
					break

	except FileNotFoundError as e:            
		try:        
			# Create a socket on the proxyserver
			# Fill in start 
			serverFacingSocket = socket(AF_INET, SOCK_STREAM)
			# Fill in end
			
			# Connect to the socket to port 80
			# Fill in start 
			serverFacingSocket.connect((webServer, port))
			print(f"Connected to {webServer}")
			serverFacingSocket.send(message.encode())
			print(f"Sent a request to {webServer}")
			# Fill in end

			with open(file_to_use, "wb") as cacheFile:
				print("Writing to cacheFile...")
				while True:
					# Fill in start
					buff = serverFacingSocket.recv(4096)
					# print("Response:\n", buff)
					# Fill in end
					
					if buff:
						# Fill in start
						print("Sending buff...")
						cacheFile.write(buff)
						clientFacingSocket.send(buff)
						print("Sent buff...")
						# Fill in end
					else:
						break
				print("Closing cacheFile...")
		except:
			print(str(sys.exc_info()[0]))                                                
		finally:
			# Fill in start     
			serverFacingSocket.close()
			print("Closed serverFacingSocket")
			# Fill in end
	except:
		print(str(sys.exc_info()[0]))

	finally:
		# Fill in start      
		clientFacingSocket.close()
		print("Closed clientFacingSocket")
		# Fill in end

if len(sys.argv) > 2:
	print('Usage : "python proxy.py port_number"\n')
	sys.exit(2)
if len(sys.argv) == 2:
	proxy_port = int(sys.argv[1])

if not os.path.exists(cache_directory):
	os.makedirs(cache_directory)
	
# Create a server socket, bind it to a port and start listening
# Fill in start             
welcomeSocket = socket(AF_INET, SOCK_STREAM)
welcomeSocket.bind((proxy_ip,proxy_port))
welcomeSocket.listen(1)
# Fill in end

print('Proxy ready to serve at port', proxy_port)

try: 
	while True:
		# Start receiving data from the client
		# Fill in start 
		clientFacingSocket, addr = welcomeSocket.accept()
		# print('Received a connection from:', addr)
		# Fill in end

		# the following function starts a new thread, taking the function name as the first argument, and a tuple of arguments to the function as its second argument
		thread.start_new_thread(client_thread, (clientFacingSocket, ))

except KeyboardInterrupt:
	print('bye...')

finally:
	# Fill in start 
	welcomeSocket.close()
	# Fill in end
