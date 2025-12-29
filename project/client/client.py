import socket
import sys
import threading
from crypto_utils import *

stop_event = threading.Event()
counter = 0


def recv_loop(sock, otp_key, mac_key):
    global counter
    while not stop_event.is_set():
        try:
            data = sock.recv(4096)
            if not data:
                break

            msg = verify_then_decrypt(otp_key, mac_key, data, counter).decode()
            counter += len(msg)

            if msg == "EndSession":
                print("\n[!] Session ended by server")
                stop_event.set()
                break

            print(f"\n[server] {msg}")

        except Exception as e:
            print(f"\n[!] Connection error: {e}")
            break

    stop_event.set()


def main():
    global counter
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        return

    host, port = sys.argv[1], int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # --- ClientHello ---
    priv = dh_generate_private()
    pub = dh_generate_public(priv)
    s.sendall(f"ClientHello:{pub}\n".encode())

    # --- ServerHello ---
    data = b""
    while not data.endswith(b"\n"):
        chunk = s.recv(1)
        if not chunk:
            print("[!] Connection closed by server")
            return
        data += chunk

    line = data.decode().strip()

    if line == "ServerFull":
        print("[!] Server is full")
        s.close()
        return

    if not line.startswith("ServerHello:"):
        print(f"[!] Unexpected server response: {line}")
        s.close()
        return

    server_pub = int(data.decode().split(":")[1])

    shared = dh_compute_shared(server_pub, priv)
    otp_key, mac_key = derive_keys(shared)

    print("[+] Secure session established", flush=True)

    threading.Thread(target=recv_loop, args=(s, otp_key, mac_key), daemon=True).start()

    while not stop_event.is_set():
        try:
            cmd = input(">> ")
        except EOFError:
            print("\n[!] EOF detected, closing client")
            break

        if stop_event.is_set():
            break
        encrypted = encrypt_then_mac(otp_key, mac_key, cmd.encode(), counter)
        counter += len(cmd)
        s.sendall(encrypted)

        if cmd == "EndSession":
            stop_event.set()
            break

    s.close()
    print("[+] Client terminated")


if __name__ == "__main__":
    main()
