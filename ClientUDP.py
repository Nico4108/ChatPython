import socket

print('Starting Client Server...')

# Messages counter
mc = 0

# Creating a UPD socket using .SOCK_DGRAM
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Get the hostname, IP Address from socket and sets Portnumber
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
lc = 'LocalHost'
port = 5052

# Setting the server address to localhost
s_addr = (lc, port)

Ccom = "C: com -"
Scom = "S: com -"
msg = "msg"

# Using .sendto to let the server know it wants to connect
sent = soc.sendto('{}'.format(ip).encode(), s_addr)

accpt, address = soc.recvfrom(5000)

while True:
    if accpt.startswith(b'accepted'):

        # print('You have been', accpt.decode(), 'by the server!')

        sentaccpt = soc.sendto(Ccom.encode(), s_addr)

        # Input field for username on client side
        name = input('Enter unsername: ')
        print('{} has joined...'.format(name))
        # Using .sendto to send username to server
        sent = soc.sendto(name.encode(), s_addr)

        # Loop to check for messages
        while True:

            message = input('\nEnter Messages: ')
            print(name, ':', message)

            # Sends out messages to server using .sendto and using .encode to convert it to bytes.
            sentMessages = soc.sendto(message.encode(), s_addr)
            # Adds 1 to messages send
            mc += 1

            # Receives messages from server using .recv and making it readable using .decode
            Smessages, server = soc.recvfrom(5000)
            print('Server :', '{}'.format(Smessages.decode()))
            mc += 1

    else:
        print('You were not accepted by server, goodbye!')
        break
