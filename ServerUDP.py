import socket

print('Setup Server...')

# Server name
name = "The Coolest Server on : "

# Creating a UPD socket using .SOCK_DGRAM and sets Port number
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5052
lc = 'LocalHost'
# Setting the server address to localhost and what port it's running on
s_addr = (lc, port)
# Using .bind to 'bind' the server to the socket
soc.bind(s_addr)
print(name, s_addr)

print("Waiting for Client connections....")
sent = soc.recv(5000)

C_ip = sent.decode()

nsent = sent.decode().split('.', 3)

print(nsent)

print(nsent[0], nsent[1], nsent[2], nsent[3])

firstIPNumber = (int(nsent[0]))
secoundIPNumber = (int(nsent[1]))
thirdIPNumber = (int(nsent[2]))
fourthIPNumber = (int(nsent[3]))

print(firstIPNumber, secoundIPNumber, thirdIPNumber, fourthIPNumber)

if (firstIPNumber <= 255) and (secoundIPNumber <= 255) and (thirdIPNumber <= 255) and (fourthIPNumber <= 255):

    print('Client IP address found:', C_ip)

else:
    print("No good ip")

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
