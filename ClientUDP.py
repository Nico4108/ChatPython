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
max_pack = parser.getboolean('Maximum', 'Start')


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
            if not parser.getboolean('Maximum', 'Start'):
                global heartbeat_
                # Sets heartbeat_ field to status from config (true or false)
                heartbeat_ = parser.getboolean('Heartbeat', 'KeepALive')
                # Calls heartbeat
                heartbeat()
                # Check if heartbeat timer is equal to correct time (3 seconds) in config file
                # and calls the proper function
                if parser.getint('Heartbeat', 'Time') == 3:
                    messagesLoop()
                else:
                    listenForMsg()
            else:
                heartbeat_ = parser.getboolean('Heartbeat', 'KeepALive')
                heartbeat()
                maxpackages()

    finally:
        # If connection to server not accepted close
        if messagesLoop() == False and parser.getboolean('Maximum', 'Start') == False:
            print('SOCKET ERROR!')
            soc.close()
            exit()


# function that only listens for msg from server
def listenForMsg():

        while True:
            resp, server = soc.recvfrom(4096)
            server_resp = resp.decode()
            # Check for proper msg received and sends back inactivity msg to client and closes client socket
            if server_resp.startswith('con-res '):
                    print(server_resp)
                    _4_sec_msg = 'con-res 0xFF'
                    _4_sec = soc.sendto(_4_sec_msg.encode(), s_addr)
                    print('Disconnected for inactivity')
                    global heartbeat_
                    heartbeat_ = False
                    soc.close()
                    exit()

            else:
                print("Msg Error!")
                soc.close()
                exit()

# function with loop for messages
def messagesLoop():

        while True:
            message = input('Enter message: ')
            global mc
            msg = 'msg-' + str(mc) + '=' + message
            # Sends first 'msg-' message to server
            sent_msg = soc.sendto(msg.encode(), s_addr)
            # Receive message from server
            resp, server = soc.recvfrom(4096)
            server_resp = resp.decode()
            # Checks the proper msg received
            if server_resp.startswith('res-'):
                s_msg1 = server_resp.split('-')
                s_msg2 = s_msg1[1].split('=')

                if int(s_msg2[0]) - mc == 1 and server_resp.startswith('res-'):
                    # Gets output from server and prints it
                    print(s_msg2[1])
                    mc += 2

            else:
                print('Msg counter ERROR')
                soc.close()
                exit()


# Function for max packages sent
def maxpackages():
    while max_pack:

        # Loop to send amount from config file of msg to server
        for x in range(parser.getint('Maximum', 'MaximumPackages')):
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
        break


handshake()
