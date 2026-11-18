# Practical Work 1: TCP File Transfer

1-1 file transfer over TCP/IP in the command line (Python 3, standard library only).
One server, one client, plain sockets.

## Files

| File | Role |
| :--- | :--- |
| `server.py` | accepts one client at a time, stores the uploaded file in `received/` |
| `client.py` | uploads one file and checks the SHA-256 returned by the server |
| `common.py` | shared helpers (`recv_line`, `recv_exact`, `safe_name`) |
| `demo.sh` | runs a full localhost demo (used for the report screenshots) |

## Run

```bash
python3 server.py [port] [output_dir]     # default: 5000, received
python3 client.py <host> <port> <file>
```

Quick check: `./demo.sh`

## Protocol

```
client -> server : SEND <name> <size>\n
server -> client : OK\n   (or ERR <reason>\n)
client -> server : <size> raw bytes
server -> client : DONE <sha256>\n
```
