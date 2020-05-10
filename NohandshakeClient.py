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
_3whs = True
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


# Skipped the 3 way handshake to see if the server can handle a connection without a handshake
def handshake():
    try:

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
                    resp, server = soc.recvfrom(4096)
                    server_resp = resp.decode()
                    if '3WHE' in server_resp:
                        _3whs = False
                    else:
                        messagesLoop()


    finally:
        # If connection to server not accepted close
        if _3whs == False and parser.getboolean('Maximum', 'Start') == False:
            print('SOCKET ERROR!')
            heartbeat_ = False
            print('Could not complete handshake with server')
            soc.close()
            exit()


# function with loop for messages
def messagesLoop():

        while _3whs:
            message = input('Enter message: ')
            global mc
            msg = 'msg-' + str(mc) + '=' + message
            # Sends first 'msg-' message to server
            sent_msg = soc.sendto(msg.encode(), s_addr)
            # Receive message from server
            resp, server = soc.recvfrom(4096)
            server_resp = resp.decode()
            # Checks the proper msg received
            if 'res-' in server_resp:
                check_mc = (int(server_resp[4]))
                mc = (int(server_resp[4]) + 1)
                # Checks if msg counter in 'res-0' is valid
                if mc - check_mc == 1 and 'res-' in server_resp:
                    # Gets output from server and prints it
                    print(server_resp[6:])

            else:
                print('Msg counter ERROR')


handshake()