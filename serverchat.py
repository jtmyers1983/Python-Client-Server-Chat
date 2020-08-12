# James Myers
# Brian Peterson

import socket
import threading
import random
import sys	
# importing sys library so that we can decide if client or server based on command line input. if (len(sys.argv) > 1):
# then we are the client, else we are the server. input should be "python3 serverchat.py" 
# for server or "python3 serverchat.py + IP" for client
class Server:
	print("Server started. Waiting for connections....")
	connection_list = []
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket for TCP connection
	serverPort = 10000 # port number to connect to server
	def __init__(self): # initialize each connection as an object with its own socket
		self.serverSocket.bind(('0.0.0.0', self.serverPort)) 
		self.serverSocket.listen(1) # server will listen for connection

	def connection_manager(self, connection, address, username): # this function will be used to handle connections
		while True:
			data = connection.recv(2048)
			stringData = data.decode('utf-8')
			if stringData == ".exit":
				self.connection_list.remove(connection)
				connection.close
				print(username + " disconnected")
				break
			stringData = username + ": " + stringData
			for connection in self.connection_list:
				connection.send(bytes(stringData, 'utf-8'))
			if not data:
				self.connection_list.remove(connection)
				connection.close
				break
			

	def run_server(self):  # this function will run the server, and accept incoming connections, and direct it to the connection_handler method.
		user_list = []
		while True:
			connection, address = self.serverSocket.accept()
			username = "Guest" + str(random.randint(1, 100)) # assigns random username to client, future version will allow you to choose
			connThread = threading.Thread(target=self.connection_manager, args=(connection, address, username))
			connThread.daemon = True
			connThread.start()
			self.connection_list.append(connection)
			user_list.append((connection, username)) # list of pairs of (connection, username) of all clients on the server 
			print(username + " connected at address: " + str(address[0] + " : " + str(address[1]))) # when client connects, server side will show username, address of that client on server side 
			
						

			

class Client: # client class will contain all functions and variables related to the client side
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a socket for TCP connection
		def send_message(self):	 # function will be used to send messages to the server
			while True:
				self.clientSocket.send(bytes(input(""), 'utf-8'))
					


		def __init__(self, address): # will be used to create a thread which will be used to send messages
			print("Welcome to the chat")
			self.clientSocket.connect((address, 10000))
			inputThread=  threading.Thread(target=self.send_message)
			inputThread.daemon = True
			inputThread.start()
			while True: # nested while loop will handle incoming data from the server
				data = self.clientSocket.recv(2048)
				if not data:
					break
				print(str(data, 'utf-8'))

if (len(sys.argv) > 1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run_server()


