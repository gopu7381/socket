# first of all import the socket library
import socket
import threading
import time
flag = 1

def listen(conn):
    conn.setblocking(0)
    while flag:
        try:
            data = conn.recv(1024)
            print "\nClient >> "+data
            time.sleep(0.1)
            print "Server >> ",
            if data == "":
                print "no more data"
                break
        except socket.error as err:
            # have to increase Err 10035
            if "10035" in err:
                pass
        except socket.timeout:
            print "Timeout"
            break

def send(conn):
    conn.setblocking(0)
    try:
        while flag:
            message = raw_input("\nServer >> ")
            conn.sendall(message)
            time.sleep(0.1)
    except socket.error as err:
        # have to increase Err 10035
        if "10035" in err:
            pass
    except EOFError as err:
        print "Encountered EOF Error %s" % (err)
        pass


# next create a socket object
s = socket.socket()
print "Socket successfully created"

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345


# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print "socket bound to %s" % (port)
s.setblocking(0)
s.settimeout(60)
# put the socket into listening mode
s.listen(5)

# a forever loop until we interrupt it or
# an error occurs

# Establish connection with client.

c = None

c, addr = s.accept()
c.settimeout(60)

print 'Got connection from', addr

rx=threading.Thread(target=listen,args=(c,))
tx = threading.Thread(target=send,args=(c,))
rx.start()
tx.start()
# while True:
#     a = raw_input("press 0 to exit")
#     if int(a) == 0:
#         break

# while True:
#     except KeyboardInterrupt:

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    flag = 0
    print "Hit Interrupt"

rx.join()
tx.join()

c.send('Thank you for connecting')
raw_input("press any key to exit")
c.close()