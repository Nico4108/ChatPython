import socket, sys

# https://www.tutorialspoint.com/simple-chat-room-using-python
print('Setup Server...')

# Besked counter
m = 0

# Get the hostname, IP Address from socket and set Port
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 5052
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))

# input field to enter a username
# name = input('Enter name: ')
name = "Server"

# .listen try to locate a client connection using a socket
# (1) means only 1 client can connect to the server
soc.listen(1)
print('Waiting for incoming connections...')

# connection assigned to the socket comming from the client
# addr assigned to the IP from the client
# The socket from the client gets accepted
connection, addr = soc.accept()

# Prints when a connection is recevied from a client with its IP(addr[0]) and port(addr[1])???
print("Received connection from ", addr[0], "(", addr[1], ")\n")

# Tells the IP address from the connected on the server
# in this case both only server and 1 clients' IP address is displayed
print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]), "\n")

# get a connection from client side and receives the clients input username
client_name = connection.recv(1024)
# .decode to make it readable
client_name = client_name.decode()
print(client_name + ' has connected.')
print('Type QUIT! to disconnect from chat')

# .send sends out the 'username' in bytes(encode)
connection.send(name.encode())

# Loop to check for messages
while True:
    m += 1
    message = "[" + str(m) + "] " + "> " + "I AM A SERVER"

    # Type QUIT to disconnect from chat
    if message == 'QUIT!':
        message = 'Good Night...'
        # a messeges is send to the client using .send in bytes(.encode)
        connection.send(message.encode())
        print("\n")
        break

    # messages getting send to client using 'connection.send' in bytes(.encode)
    connection.send(message.encode())

    # Receives messages from client using .recv and makes them readable using .decode
    message = connection.recv(1024)
    message = message.decode()
    # Prints name and the messages typed
    print(client_name, message)