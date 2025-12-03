import socket
import struct
import argparse
import random
import hashlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="0.0.0.0")
parser.add_argument("--port", type=int, default=5005)
parser.add_argument("--loss", type=int, default=0, help="packet loss percent 0-100")
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((args.host, args.port))
print(f"Server listening on {args.host}:{args.port}, loss={args.loss}%")

chunks = {}
expected_total = None

while True:
    data, addr = sock.recvfrom(1500)

    if random.randrange(100) < args.loss:
        print(f"Simulated drop of packet from {addr}")
        continue

    if len(data) < 6:
        print("Too short packet")
        continue

    seq, plen = struct.unpack("!IH", data[:6])
    payload = data[6:6+plen]

    if len(payload) != plen:
        print(f"Payload length mismatch for seq {seq}")
        continue

    if seq not in chunks:
        chunks[seq] = payload
        print(f"Received seq={seq} len={plen} total_received={len(chunks)}")

    ack = struct.pack("!I", seq)
    sock.sendto(ack, addr)

    if expected_total is None and len(chunks) >= 100:
        expected_total = 100
    if expected_total is not None and len(chunks) >= expected_total:
        break

with open("received.bin", "wb") as f:
    for i in range(expected_total):
        f.write(chunks[i])

sha = hashlib.sha256()
with open("received.bin", "rb") as f:
    sha.update(f.read())
print("Server: reconstructed file 'received.bin'")
print("Server SHA256:", sha.hexdigest())
sys.exit(0)
