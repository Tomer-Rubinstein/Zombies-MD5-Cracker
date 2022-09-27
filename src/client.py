import socket
import hashlib
import json

HOST = socket.gethostname()
PORT = 3000

client_socket = socket.socket()
client_socket.connect((HOST, PORT))
client_socket.send('a'.encode())

data = json.loads(client_socket.recv(1024).decode())

md5_hash = data['md5_hash']
wordlist = data['wordlist']

res = '0;'
for word in wordlist:
  md5_word = hashlib.md5(word.encode('utf-8')).hexdigest()
  if md5_word == md5_hash:
    print(f"[MATCH] {word}")
    res = str(len(word)) + ';' + word
    break

client_socket.send(res.encode())
client_socket.close()
