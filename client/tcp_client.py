# simple Python socket client
# (c) G.Blinowski for PSI 2021

import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address

if  len(sys.argv) < 3: 
  print("no port and/or host, using localhost:8000")
  port=8000
  host=HOST
else:
  host = sys.argv[1]
  port = int( sys.argv[2] )

print("Will connect to ", host, ":", port)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
#    s.sendall(b'0123456789')
# what happens when we send more data to server accepting only 10B at a time?
    s.sendall(b'Hello, world!')
    data = s.recv(1024)

print('Received', repr(data))
print('Client finished.')

