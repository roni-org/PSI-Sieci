# simple Python socket client
# (c) G.Blinowski for PSI 2021

import sys, array, struct
from socket import *


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
BUFSIZE = 512
TIMEOUT = 5.0
# BUFSIZE =10 

def moreWork(): 
  return True

def moreData():
  return True

def main():
  if  len(sys.argv) < 2:
    print("no port, using 8000")
    port=8000
  else:
    port = int( sys.argv[1] )

  # host will always default to current host name
  host = gethostname()
  print("Will listen on ", host, ":", port)

  s = socket(AF_INET, SOCK_STREAM)
  s.bind((host, port))
  s.settimeout( TIMEOUT )
  # if backlog is specified, it must be at least 0 (if it is lower, it is set to 0); 
  # it specifies the number of unaccepted connections that the system will allow 
  # before refusing new connections
  s.listen( 5 )
  while moreWork():
        try:
  # The return value is a pair (conn, address) where conn is a new socket object 
  # and address is the address bound to the socket on the other end of the connection.
            conn, addr = s.accept()
        except timeout:
            print("accept() timeout, restarting...")
            continue
        except KeyboardInterrupt:
            print("accept() interrupted, ending.")
            sys.exit(1)
        with conn:
            print('Connect from: ', addr)
            while moreData():
                data = conn.recv( BUFSIZE )
                if not data:
                    break
  # echo back data - NOTE - compare send() and sendall()!
                conn.sendall(data)
        conn.close()
        print("Connection closed by client" )

if __name__ == "__main__":
    main()

