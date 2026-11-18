"""Shared helpers for the TCP file-transfer protocol.

Protocol (text header line + raw bytes):
  client -> server : "SEND <filename> <size>\n"
  server -> client : "OK\n"            (or "ERR <reason>\n" then close)
  client -> server : <size> raw bytes
  server -> client : "DONE <sha256>\n"  (client compares with its own hash)
"""
import os

CHUNK = 64 * 1024


def recv_line(sock):
    """Read bytes up to and including '\\n'; return the line without it."""
    buf = bytearray()
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError("connection closed while reading line")
        if b == b"\n":
            return buf.decode()
        buf += b
        if len(buf) > 4096:
            raise ValueError("header too long")


def recv_exact(sock, n):
    """Yield chunks until exactly n bytes have been received."""
    while n > 0:
        data = sock.recv(min(CHUNK, n))
        if not data:
            raise ConnectionError("connection closed mid-transfer")
        n -= len(data)
        yield data


def safe_name(name):
    """Strip any directory part so a client cannot write outside the target dir."""
    return os.path.basename(name.replace("\\", "/"))
