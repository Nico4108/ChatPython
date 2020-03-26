import socket

print('Setup Server...')

# Besked counter
m = 0

# Server name
name = "The Coolest Server on : "


# Creating a UPD socket using .SOCK_DGRAM and sets Port number
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5052
lc =  'LocalHost'
# Setting the server address to localhost and what port it's running on
s_addr = (lc, port)
# Using .bind to 'bind' the server to the socket
soc.bind(s_addr)
print(name, s_addr)

sent = soc.recvfrom(5000)

# Use .recv to get the clients username and prints it
c_name = soc.recv(5000)
print(c_name.decode(), ':', ' has connected.')

# Loop to check for messages
while True:

    print('\nWaiting to receive message from Client:')
    # Cmessages is the clients input and where it is stored and then printed
    Cmessages, address = soc.recvfrom(5000)
    print(c_name.decode(), ':', Cmessages.decode())

    if Cmessages:
        # The server sends back a automated reply using .sendto and .encode to convert it to bytes.
        sent = soc.sendto('I AM A SERVER!!'.encode(), address)