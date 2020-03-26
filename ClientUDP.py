import socket

print('Starting Client Server...')

# Besked counter
m = 0

# Creating a UPD socket using .SOCK_DGRAM
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Get the hostname, IP Address from socket and sets Portnumber
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
lc = 'LocalHost'
port = 5052

# printing the information from server
print(shost, '({})'.format(ip))

# Setting the server address to localhost
s_addr = (lc, port)

# Using .sendto to let the server know it wants to connect
sent = soc.sendto('Connection Request send'.encode(), s_addr)

# Input field for username on client side
name = input('Enter unsername: ')
print('{} has joined...'.format(name))
# Using .sendto to send username to server
sent = soc.sendto(name.encode(), s_addr)

# Loop to check for messages
while True:

    message = input('\nEnter Messages: ')
    print('[', m, '] ', name, ':', message)

    # Type QUIT to disconnect from chat
    if message == "QUIT!":
        # Use .sendto to send a messages to the server telling it that the client has disconnected
        message = "LEFT THE CHAT ROOM!!"
        soc.sendto(message.encode(), s_addr)
        print("GOODBYE!")
        # Terminates class
        break

    # Sends out messages to server using .sendto and using .encode to convert it to bytes.
    sentMessages = soc.sendto(message.encode(), s_addr)
    # Adds 1 to messages send
    m += 1

    # Receives messages from server using .recv and making it readable using .decode
    Smessages, server = soc.recvfrom(5000)
    print('[', m, '] ', 'Server Responds: {}'.format(Smessages.decode()))
    m += 1


