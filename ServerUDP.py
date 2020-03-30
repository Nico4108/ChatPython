import socket

print('Setup Server...')

# Server name
name = "The Coolest Server on : "

Ccom = "C: com -"
Scom = "S: com -"
msg = "C: msg -"
res = "S: res -"

mc = 0

# Creating a UPD socket using .SOCK_DGRAM and sets Port number
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5052
lc = 'LocalHost'
ip = socket.gethostbyname(lc)
# Setting the server address to localhost and what port it's running on
s_addr = (lc, port)
# Using .bind to 'bind' the server to the socket
soc.bind(s_addr)
print(name, s_addr)

print("Waiting for Client connections....")

while True:
    sent = soc.recv(5000)

    # Receives IP address from client
    C_ip = sent.decode()

    print(Ccom, mc, '<{}>'.format(C_ip))

    # Split IP address
    nsent = sent.decode().split('.', 3)

    # Converts IP from str to int
    firstIPNumber = (int(nsent[0]))
    secoundIPNumber = (int(nsent[1]))
    thirdIPNumber = (int(nsent[2]))
    fourthIPNumber = (int(nsent[3]))

    # Checks if received IP address is legal
    if (0 <= firstIPNumber <= 255) and (0 <= secoundIPNumber <= 255) and (0 <= thirdIPNumber <= 255) and (0 <= fourthIPNumber <= 255):

        print(Scom, mc, 'Accept', '<{}>'.format(ip))

        # Sends back a accpted messages to client using .sendto
        accpt, address = soc.recvfrom(5000)
        accpt = soc.sendto('accepted'.encode(), address)

        aceptsent = soc.recv(5000)
        if aceptsent.startswith(b'C:'):
            print(aceptsent.decode(), mc, 'Accept')

            # Use .recv to get the clients username and prints it
            c_name = soc.recv(5000)
            print(Scom, mc, c_name.decode(), ':', 'has connected.')

            mc += 1

    else:
        print("No good ip")

    # Loop to check for messages
    while True:
        print('\nWaiting to receive message from Client:')
        # Cmessages is the clients input and where it is stored and then printed
        Cmessages, address = soc.recvfrom(5000)
        if mc < 1:
            print('Counter error!')
        else:
            print(msg, mc, c_name.decode(), ':', Cmessages.decode())
            mc += 1
            print(res, mc, 'I AM A SERVER!')

        if Cmessages:
            # The server sends back a automated reply using .sendto and .encode to convert it to bytes.
            sent = soc.sendto('I AM A SERVER!!'.encode(), address)

