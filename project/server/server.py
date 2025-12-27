import socket
import threading
import sys
from project.crypto_utils import *

clients = {}
lock = threading.Lock()
client_id_counter = 0


def recv_line(conn):
    buf = b""
    while True:
        part = conn.recv(1)
        if not part:
            return None
        if part == b"\n":
            break
        buf += part
    return buf.decode()


def handle_client(conn, addr):
    global client_id_counter
    counter = 0
    print(f"[+] Client connected: {addr}", flush=True)

    # --- ClientHello ---
    data = recv_line(conn)
    if not data or not data.startswith("ClientHello"):
        conn.close()
        return

    client_pub = int(data.split(":")[1])

    # --- ServerHello ---
    server_priv = dh_generate_private()
    server_pub = dh_generate_public(server_priv)
    conn.sendall(f"ServerHello:{server_pub}\n".encode())

    shared = dh_compute_shared(client_pub, server_priv)
    otp_key, mac_key = derive_keys(shared)

    with lock:
        client_id_counter += 1
        cid = client_id_counter
        clients[cid] = {
            "addr": addr,
            "conn": conn,
            "otp": otp_key,
            "mac": mac_key,
            "counter": 0,
        }

    print(f"[+] Client ID={cid} from {addr}", flush=True)

    while True:
        try:
            encrypted = conn.recv(4096)
            if not encrypted:
                break

            with lock:
                counter = clients[cid]["counter"]

            msg = verify_then_decrypt(otp_key, mac_key, encrypted, counter).decode()

            with lock:
                clients[cid]["counter"] += len(msg)

            if msg == "EndSession":
                print(f"[-] Session ended: {cid}", flush=True)
                break

            print(f"[{cid}] {msg}", flush=True)

        except Exception as e:
            print(f"[!] Error {cid}: {e}", flush=True)
            break

    with lock:
        clients.pop(cid, None)
    conn.close()
    print(f"[-] Client {cid} disconnected", flush=True)


def server_console():
    while True:
        cmd = input("server> ").strip()

        if cmd == "list":
            with lock:
                for cid, c in clients.items():
                    print(f"ID={cid} addr={c['addr']}")
            continue

        if cmd.startswith("EndSession "):
            try:
                cid = int(cmd.split()[1])
            except:
                print("Usage: EndSession <client_id>")
                continue

            with lock:
                client = clients.get(cid)

            if not client:
                print("No such client")
                continue

            try:
                otp_key = client["otp"]
                mac_key = client["mac"]
                counter = client["counter"]
                msg = encrypt_then_mac(otp_key, mac_key, b"EndSession", counter)
                client["conn"].sendall(msg)
                client["counter"] += len(b"EndSession")
                print(f"[+] Sent EndSession to client {cid}")
            except Exception as e:
                print(f"[!] Error ending session with client {cid}: {e}")

        else:
            print("Commands: list | EndSession <id>")


def main():
    if len(sys.argv) != 3:
        print("Usage: python server.py <port> <max_clients>")
        return

    port = int(sys.argv[1])
    max_clients = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(max_clients)

    print(f"[+] Server listening on port {port}", flush=True)
    threading.Thread(target=server_console, daemon=True).start()

    while True:
        conn, addr = s.accept()
        with lock:
            if len(clients) >= max_clients:
                print(f"[!] Rejecting {addr} (server full)", flush=True)
                conn.sendall(b"ServerFull\n")
                conn.close()
                continue

        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
