import socket
import sys
import time
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# HOST = "127.0.0.1"  # The server's hostname or IP address
HOST = "pserver1"  # The server's hostname or IP address
DEFAULT_PORT = 8000

if len(sys.argv) < 3:
    print("no port and/or host, using localhost:8000")
    port = 8000
    host = HOST
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

print(f"Will send to {HOST}:{port}")

sizes = [2**i for i in range(1, 16)] + [
    40000,
    50000,
    60000,
    65000,
    65500,
    65507,
    65508,
]
times = []

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(1)
    for size in sizes:
        data = b"a" * size
        print(f"Sending buffer size = {size} bytes")
        start = time.time()
        try:
            try:
                sock.sendto(data, (HOST, port))
            except OSError as e:
                print(f"Cannot send {size} bytes: {e}")
                break
            resp, _ = sock.recvfrom(1024)
            end = time.time()
            elapsed = (end - start) * 1000
            times.append(elapsed)
            print(f"Received {len(resp)} bytes, elapsed time = {elapsed:.2f} ms")
        except socket.timeout:
            print(f"Timeout for {size} bytes")
            times.append(None)


plt.plot(sizes[: len(times)], times, marker="o")
plt.xlabel("Datagram size (B)")
plt.ylabel("Answer time (ms)")
plt.title("zad 1.1")
plt.xscale("log", base=2)
plt.grid(True)
plt.savefig("/output/zad1_1.png")

print("Client finished.")
