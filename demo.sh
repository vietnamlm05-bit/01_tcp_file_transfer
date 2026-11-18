#!/usr/bin/env bash
# Runs one full demo on localhost: start server, upload 2 files, verify, test an error.
cd "$(dirname "$0")"
PORT=5000
rm -rf received; head -c 1048576 /dev/urandom > samples/big.bin

python3 -u server.py $PORT received > /tmp/tcp_demo_server.log 2>&1 &
SERVER=$!; sleep 1

echo "=== CLIENT: upload ==="
for f in samples/hello.txt samples/big.bin; do
  echo "\$ python3 client.py 127.0.0.1 $PORT $f"
  python3 client.py 127.0.0.1 $PORT $f | tail -1
done
echo; echo "=== CLIENT: malformed request ==="
printf 'garbage\n' | timeout 2 nc 127.0.0.1 $PORT
sleep 0.5; kill $SERVER

echo; echo "=== SERVER LOG ==="; cat /tmp/tcp_demo_server.log
echo; echo "=== INTEGRITY (md5sum) ==="
for n in hello.txt big.bin; do
  md5sum samples/$n received/$n
done
