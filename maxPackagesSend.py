import multiprocessing
import socket
import threading
from configparser import ConfigParser

# Field to read and get config file
parser = ConfigParser()
parser.read('con.ini')

# Creating a UPD socket using .SOCK_DGRAM
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Get the hostname, IP Address from socket and sets Portnumber
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
lc = 'LocalHost'
port = 5052
# Setting the server address to localhost
s_addr = (lc, port)
# Messages counter
mc = 0
max_pack = True


# Heartbeat function
def heartbeat():

    if heartbeat_:
        # i as interval in seconds
        threading.Timer(parser.getint('Heartbeat', 'Time'), heartbeat).start()
        # put your action here
        hb_msg = 'con-h 0x00'
        hb_msg_sent = soc.sendto(hb_msg.encode(), s_addr)

    else:
        print("Heartbeat not activated")
        soc.close()
        exit()


# 3 way handshake function
def handshake():
    try:

        # first com-0 conncetion send to server
        con_requ = 'com-' + str(mc) + ' ' + ip
        # Using .sendto to let the server know it wants to connect
        sent_con_requ = soc.sendto(con_requ.encode(), s_addr)

        info, server = soc.recvfrom(4096)
        # get com-0 accept from server
        info_string = info.decode()
        ip_split = info_string.replace('com-0 accept ', '')
        s_ip = ip_split
        # Checks it messages contains 'com-0 accept' and that the IP is valid
        if info_string.startswith('com-0 accept') and socket.inet_aton(s_ip):
            client_accept = 'com-' + str(mc) + ' accept'
            sent = soc.sendto(client_accept.encode(), s_addr)
            # Checks if max packages it set to False in config file
            global heartbeat_
            heartbeat_ = parser.getboolean('Heartbeat', 'KeepALive')
            heartbeat()
            maxpackages()

    finally:
        # If connection to server not accepted close
        if max_pack == False and parser.getboolean('Maximum', 'Start') == False:
            print('SOCKET ERROR!')
            soc.close()
            exit()


# Function that send 100 packages to server and see if the server lets it handle that.
def maxpackages():

    while max_pack:

        # Loop to send amount of msg to server
        for x in range(100):
            msg = 'msg-' + str(mc) + '='

            # Uses multiprocessing to send x amount of msg to server
            mp = multiprocessing.Process(target=soc.sendto, args=(msg.encode(), s_addr))
            mp.start()

        # Receives response from from server and closes client socket
        resp, server = soc.recvfrom(4096)
        server_resp = resp.decode()
        print(server_resp)
        global heartbeat_
        heartbeat_ = False
        soc.close()
        exit()


handshake()
