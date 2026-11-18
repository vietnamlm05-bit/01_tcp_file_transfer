#!/usr/bin/env python3
"""TCP file-transfer client: uploads one file to the server.
Usage: client.py <host> <port> <file>"""
import hashlib
import os
import socket
import sys

from common import CHUNK, recv_line


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    host, port, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    name = os.path.basename(path)
    size = os.path.getsize(path)

    with socket.create_connection((host, port)) as s:
        s.sendall(f"SEND {name} {size}\n".encode())
        reply = recv_line(s)
        if reply != "OK":
            sys.exit(f"server refused: {reply}")

        sha = hashlib.sha256()
        sent = 0
        with open(path, "rb") as f:
            while chunk := f.read(CHUNK):
                s.sendall(chunk)
                sha.update(chunk)
                sent += len(chunk)
                print(f"\rsent {sent}/{size} bytes", end="", flush=True)
        print()

        reply = recv_line(s).split(" ")
        if reply[0] == "DONE" and reply[1] == sha.hexdigest():
            print("transfer OK, SHA-256 matches")
        else:
            sys.exit(f"transfer FAILED: {' '.join(reply)}")


if __name__ == "__main__":
    main()
