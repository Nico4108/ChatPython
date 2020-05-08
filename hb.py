import threading

"""def looper():
    # i as interval in seconds
    threading.Timer(3, looper).start()
    # put your action here
    print('con-h 0x00')

#to start
looper()
"""
import time
import threading

def countdown():
    global my_timer
    my_timer = 0
    while my_timer < 11:
        time.sleep(1)
        my_timer += 1
        print(my_timer)
        m = input("test: ")

    print("done countdown")


countdown_thread = threading.Thread(target=countdown)
countdown_thread.start()

"""threading.Timer(11, check_4_seconds).start()

    messages_4_sec, address = soc.recvfrom(4096)
    test_heartbeat_msg = messages_4_sec.decode()
    print(test_heartbeat_msg, 117)

    if 'death' in test_heartbeat_msg:
        _4_sec_msg = 'con-res 0xFE'
        _4_sec_resp = soc.sendto(_4_sec_msg.encode(), address)

        death_note = messages_4_sec.decode()
        print(death_note)"""