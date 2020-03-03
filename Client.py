import time, socket, sys

print('Starting Client Server...')

# time.sleep(1)

# Get the hostname, IP Address from socket and set Port
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)

# printing the information to connect to the server
print(shost, '({})'.format(ip))

# input field to enter the IP address from the server
server_host = input('Enter server\'s IP address:')

# input field to enter a username
name = input('Enter Client\'s name: ')
port = 1235
print('Trying to connect to the server: {}, ({})'.format(server_host, port))

# time.sleep(1)

# using '.connect' to connect to the server after getting the IP address and port number
soc.connect((server_host, port))
print("You are now connected...\n")

# Using .send to send out the 'username' in bytes(encode)
soc.send(name.encode())
# gets a connection from server side and receives the serves input username
server_name = soc.recv(1024)
# .decode to make it readable
server_name = server_name.decode()
print('{} has joined...'.format(server_name))
print('Type QUIT! to discconect form chat')

# Loop to check for messages
while True:
    # receives messages from server using .recv and making it readable using .decode
    message = soc.recv(1024)
    message = message.decode()
    print(server_name, ">", message)
    # input field to response
    message = input(str("Me > "))

    # Type QUIT to disconnect from chat
    if message == "QUIT!":
        message = "left the Chat room"
        soc.send(message.encode())
        print("\n")
        break
    # Using .send to send out the message in bytes(encode) to server
    soc.send(message.encode())
