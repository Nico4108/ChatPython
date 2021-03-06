import socket
import datetime
import re

# Creating a UPD socket using .SOCK_DGRAM and sets Port number
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5052
lc = 'LocalHost'
ip = socket.gethostbyname(socket.gethostname())
# Setting the server address to localhost and what port it's running on
s_addr = (lc, port)
# Using .bind to 'bind' the server to the socket
soc.bind(s_addr)
packages_count = 0
mc = 1
dt = datetime.datetime.now()


# Function for 3 way handshake
def _3whs_connection():
    # First connection form client received 'com-0'
    info, address = soc.recvfrom(4096)
    first_info = info.decode()
    print(first_info)
    # Separates ip from message
    ip_split = first_info.replace('com-0 ', '')
    c_ip = ip_split
    # Checks if messages received contains 'com-0' and if IP is valid
    if first_info.startswith('com-0') and socket.inet_aton(c_ip):
        server_accepts_client = 'com-0 accept' + ' ' + ip
        # Sends back 'com-0 accept' to client
        sent = soc.sendto(server_accepts_client.encode(), address)
        print(server_accepts_client)
        # Third 'com-0' messages received from client
        info2, address = soc.recvfrom(4096)

        if info2.decode().startswith('com-0 accept'):

            f = open('Log.txt', 'a')
            f.write("Handshake successful : " + str(dt) + " : " + c_ip + "\n")
            f.close()

            print(info2.decode())
            soc.settimeout(4)
            _1st_msg_checkup()

    else:
        # 3WHE = 3 whay handshake error
        handshakeError = '3WHE'
        soc.sendto(handshakeError.encode(), address)
        print('3 way Handshake ERROR')

        f = open('Log.txt', 'a')
        f.write("Handshake unsuccessful : " + str(dt) + " : " + c_ip + "\n")
        f.close()
        #_3whs_connection()


# Function check if first message is valid by 'msg-0'
def _1st_msg_checkup():
    global address
    try:
        message, address = soc.recvfrom(4096)
        message_from_client = message.decode()

        # Checks if message from client contains 'msg-0'
        if message_from_client.startswith('msg-0'):
            # Gives and sets the messages from client to next Functions(messages_sent) parameter
            messages_sent(message_from_client, address)
            msg_fnkt()
        # Checks if message from client contains 'con-h' for heartbeat
        elif message_from_client.startswith('con-h'):
            messages_sent(message_from_client, address)
            msg_fnkt()
        else:
            print('Msg counter ERROR 2')


    # If no messages received before 4 seconds disconnect client
    except socket.timeout:

        _4_sec_inactive_msg = 'con-res 0xFE'
        _4_sec_inactive_resp = soc.sendto(_4_sec_inactive_msg.encode(), address)

        messages_4_sec_inactive, address = soc.recvfrom(4096)
        _4_sec_inactive_resp_client = messages_4_sec_inactive.decode()
        print("Client disconnected for inactivity " + _4_sec_inactive_resp_client)
        soc.close()
        exit()


# Function for sending automated reply to client
def messages_sent(msg_from_client, c_address):

    if msg_from_client.startswith('msg-'):
        c_msg1 = msg_from_client.split('-')
        c_msg2 = c_msg1[1].split('=')
        global mc
        reply = 'res-' + str(mc) + '=I am server'
        if mc - int(c_msg2[0]) == 1 and msg_from_client.startswith('msg-'):
            # Automated reply 'I am server' send back to client
            respond_to_client = soc.sendto(reply.encode(), c_address)
            mc += 2
        else:
            print('Msg counter ERROR 3')
            m_e = 'Msg counter ERROR 3'
            soc.sendto(m_e.encode(), c_address)
            soc.close()
            exit()

    elif msg_from_client.startswith('con-h'):
        print('client alive: ' + msg_from_client)

    # Checks if message from client contains 'com-' from max packages
    elif msg_from_client.startswith('com-'):
        global packages_count
        packages_count += 1
        #print(msg_from_client)
        if packages_count >= 25:
            _max_pac = 'Maximum 25 packages allowed'
            _max_pac_resp = soc.sendto(_max_pac.encode(), address)
            print('Server received over max limit packages!')
            soc.close()
            exit()

    else:
        print(msg_from_client)
        print('Msg counter ERROR 3')
        soc.close()
        exit()


# Receive and read client message and send it to Function(messages_sent)
def msg_fnkt():
    while True:
        messages, address = soc.recvfrom(4096)
        # Receive and decodes client message
        msg_from_client = messages.decode()
        messages_sent(msg_from_client, address)


_3whs_connection()
