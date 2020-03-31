import socket

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
_3whs = False

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
    if "com-0 accept" in info_string and socket.inet_aton(s_ip):
        client_accept = 'com-' + str(mc) + ' accept'
        sent = soc.sendto(client_accept.encode(), s_addr)
        _3whs = True

finally:
    # If connection to server not accepted close
    if not _3whs:
        print('SOCKET ERROR!')
        soc.close()
        exit()

# loop for messages
while _3whs:
    message = input('Enter message: ')
    msg = 'msg-' + str(mc) + '=' + message
    # Sends first 'msg-' message to server
    sent_msg = soc.sendto(msg.encode(), s_addr)
    # Receive message from server
    resp, server = soc.recvfrom(4096)
    server_resp = resp.decode()
    check_mc = int(server_resp[4])
    mc = (int(server_resp[4]) + 1)
    # Checks if msg counter in 'res-0' is valid
    if mc - check_mc == 1 and 'res-' in server_resp:
        # Gets output from server and prints it
        print(server_resp[6:])
    else:
        print('Msg counter ERROR')
