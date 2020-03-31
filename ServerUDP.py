import socket

# Creating a UPD socket using .SOCK_DGRAM and sets Port number
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5052
lc = 'LocalHost'
ip = socket.gethostbyname(socket.gethostname())
# Setting the server address to localhost and what port it's running on
s_addr = (lc, port)
# Using .bind to 'bind' the server to the socket
soc.bind(s_addr)


def _3whs_connection():

    # First connection form client received 'com-0'
    info, address = soc.recvfrom(4096)
    first_info = info.decode()
    print(first_info)
    # Separates ip from message
    ip_split = first_info.replace('com-0 ', '')
    c_ip = ip_split
    # Checks if messages received contains 'com-0' and if IP is valid
    if "com-0" in first_info and socket.inet_aton(c_ip):
        server_accepts_client = 'com-0 accept' + ' ' + ip
        # Sends back 'com-0 accept' to client
        sent = soc.sendto(server_accepts_client.encode(), address)
        print(server_accepts_client)
        # Third 'com-0' messages received from client
        info2, address = soc.recvfrom(4096)
        if 'com-0 accept' in info2.decode():
            print(info2.decode())
            _1st_msg_checkup()
    else:
        print('Msg counter ERROR')


# Function check if first message is valid by 'msg-0'
def _1st_msg_checkup():
    message, address = soc.recvfrom(4096)
    message_from_client = message.decode()
    # Checks if message from client contains 'msg-0'
    if 'msg-0' in message_from_client:
        # Gives and sets the messages from client to next Functions(messages_sent) parameter
        messages_sent(message_from_client, address)
        msg_fnkt()
    else:
        print('Msg counter ERROR')


# Function for sending automated reply to client
def messages_sent(msg_from_client, c_address):
    check_mc = int(msg_from_client[4])
    mc = (int(msg_from_client[4]) + 1)
    # Checks if msg counter in 'msg-0' is valid
    if mc - check_mc == 1 and 'msg-' in msg_from_client:
        reply = 'res-' + str(mc) + '=I am server'
        # Automated reply 'I am server' send back to client
        respond_to_client = soc.sendto(reply.encode(), c_address)
    else:
        print('Msg counter ERROR')


# Receive and read client message and send it to Function(messages_sent)
def msg_fnkt():
    while True:
        messages, address = soc.recvfrom(4096)
        # Receive and decodes client message
        msg_from_client = messages.decode()
        # Send message to get Checked
        messages_sent(msg_from_client, address)


_3whs_connection()

