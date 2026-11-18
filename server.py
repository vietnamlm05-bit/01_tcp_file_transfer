#!/usr/bin/env python3
"""TCP file-transfer server: accepts one client at a time and stores uploads.
Usage: server.py [port] [output_dir]"""
import hashlib
import os
import socket
import sys

from common import recv_exact, recv_line, safe_name

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "received"


def handle(conn):
    parts = recv_line(conn).split(" ")
    if len(parts) < 3 or parts[0] != "SEND" or not parts[-1].isdigit():
        conn.sendall(b"ERR bad request\n")
        return
    size = int(parts[-1])
    name = safe_name(" ".join(parts[1:-1]))
    if not name:
        conn.sendall(b"ERR bad filename\n")
        return
    conn.sendall(b"OK\n")

    sha = hashlib.sha256()
    path = os.path.join(OUT_DIR, name)
    with open(path, "wb") as f:
        for chunk in recv_exact(conn, size):
            f.write(chunk)
            sha.update(chunk)
    conn.sendall(f"DONE {sha.hexdigest()}\n".encode())
    print(f"received {name} ({size} bytes) -> {path}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"listening on {HOST}:{PORT}, saving to {OUT_DIR}/")
        while True:
            conn, addr = srv.accept()
            print(f"connection from {addr[0]}:{addr[1]}")
            with conn:
                try:
                    handle(conn)
                except (ConnectionError, ValueError, OSError) as e:
                    print(f"transfer failed: {e}")


if __name__ == "__main__":
    main()
