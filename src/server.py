import socket
import threading
import sys
import math
import json

ASCII_ART = """
            ______                                __                           
           /      \                              |  \                          
 ________ |  $$$$$$\  ______   ______    _______ | $$   __   ______    ______  
|        \| $$   \$$ /      \ |      \  /       \| $$  /  \ /      \  /      \ 
 \$$$$$$$$| $$      |  $$$$$$\ \$$$$$$\|  $$$$$$$| $$_/  $$|  $$$$$$\|  $$$$$$\ 
  /    $$ | $$   __ | $$   \$$/      $$| $$      | $$   $$ | $$    $$| $$   \$$
 /  $$$$_ | $$__/  \| $$     |  $$$$$$$| $$_____ | $$$$$$\ | $$$$$$$$| $$      
|  $$    \ \$$    $$| $$      \$$    $$ \$$     \| $$  \$$\ \$$     \| $$      
 \$$$$$$$$  \$$$$$$  \$$       \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$      
   
                                                                               """

class Server:
  def __init__(self, host, port):
    self.HOST = host
    self.PORT = port
    self.zombies = {}
    self.isCollecting = False


  def init_server(self):
    self.server_socket = socket.socket()
    self.server_socket.bind((self.HOST, self.PORT))


  def collect_zombies(self):
    self.server_socket.listen() # TODO: argparse to instruct how many connections can be accepted
    self.isCollecting = True

    while self.isCollecting:
      zombie_socket, zombie_addr = self.server_socket.accept()
      if zombie_socket.recv(3).decode() == 'end':
        break
      self.zombies[zombie_addr] = zombie_socket # TODO: handle client disconnections
      print(f"[+] New connection established from {zombie_addr[0]}")


  def stop_collecting(self):
    self.isCollecting = False
    # sending a "end of listening" signal to the server socket
    # in order to kill the last accept() thread
    t_socket = socket.socket()
    t_socket.connect((self.HOST, self.PORT))
    t_socket.send('end'.encode())
    t_socket.close()


  # divide work & start bruteforcing
  def start_cracking(self, wordlist_path, md5_hash):
    if len(self.zombies) == 0:
      print("Not enough zombies were collected to start cracking (0)")
      sys.exit()

    # NOTE: assuming all words are newline-seperated.
    with open(wordlist_path, 'r') as file:
      words = [word.strip('\n') for word in file.readlines()]
      n = len(words)
      k = len(self.zombies)
      for i,j in enumerate(self.zombies):
        currSlice = words[math.floor(i/k*n):math.floor((i+1)/k*n)]
        conn = self.zombies[j]
        data = {
          "md5_hash": md5_hash,
          "wordlist": currSlice
        }
        zcomm_thread = threading.Thread(target=self.communicate_zombie, args=(conn, j, data))
        zcomm_thread.start()


  def communicate_zombie(self, conn, z_addr, data):
    # send data to client
    conn.send(json.dumps(data).encode())

    # listen for response
    respone_len = 0
    padding = 1
    while True:
      c = conn.recv(1).decode()
      if c == ';':
        break
      respone_len *= padding
      respone_len += int(c)
      padding *= 10

    response = conn.recv(respone_len).decode()
    if response.strip() != "":
      print(f"[SUCC] {z_addr[0]} successfully cracked the hash: {response[response.find(';')+1:]}")
      return

    print(f"[!] {z_addr[0]} couldn't crack the hash")


# DEBUG
if __name__ == "__main__":
  print(ASCII_ART)

  server = Server(socket.gethostname(), 3000)
  server.init_server()
  
  collect_thread = threading.Thread(target=server.collect_zombies)
  collect_thread.start()

  print("Listening for connections..\nWhen ready, enter 's' to start cracking or CTRL+C to abort")
  # TODO: show currently connected zombies (len(server.zombies))
  while True:
    try:
      if input() == 's':
        server.stop_collecting()
        server.start_cracking('wordlist.txt', '9ab6ff8d53822ff1dc8c12c9317f530c')
        break
    except KeyboardInterrupt:
      server.stop_collecting()
      sys.exit()
