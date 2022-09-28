import socket
import hashlib
import json

HOST = socket.gethostname()
PORT = 3000 # NOTE: change accordingly

client_socket = socket.socket()
client_socket.connect((HOST, PORT))
client_socket.send('a'.encode()) # dummy byte

header = ""
while True:
  c = client_socket.recv(1).decode()
  if c == ';': break
  header += c

data_len = int(header)
# recv data_len+1 bytes to avoid the terminating ';'
data = json.loads(client_socket.recv(data_len+1).decode()) # decode the JSON string to a dict

md5_hash = data['md5_hash']
wordlist = data['wordlist']

res = ""
for word in wordlist:
  # encode each word in the wordlist to MD5 and look for match
  md5_word = hashlib.md5(word.encode('utf-8')).hexdigest()
  if md5_word == md5_hash:
    print(f"[MATCH] {word}")
    res = word
    break

res += ';' # each zombie data should be terminated with ';'!
client_socket.send(res.encode())
client_socket.close()
