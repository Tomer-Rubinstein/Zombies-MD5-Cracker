import socket
import threading
import sys
import math
import json


"""
Server class is responsible for handling the communication between
the host and the zombies and for dividing the bruteforcing work between the zombies.

@params:
  - host(string), the address to bind the server to
  - port(integer), the port to listen for connections on
"""
class Server:
  def __init__(self, host: str, port: int, connlim: int):
    self.HOST = host
    self.PORT = port
    self.connlim = connlim
    self.zombies = {} # connected zombies dictionary


  """
  init_server() initializes the server socket object and binds a socket
  on the given address(HOST) and port.

  @params: None
  @return: None
  """
  def init_server(self):
    self.server_socket = socket.socket()
    self.server_socket.bind((self.HOST, self.PORT))


  """
  collect_zombies() is responsible for accepting connections on the server socket
  and for adding new zombies to the zombie dictionary.

  @params: None
  @return: None
  """
  def collect_zombies(self):
    # instruct how many connections can be accepted
    # if no connections limit was given, it will default to unlimited
    if not self.connlim:
      self.server_socket.listen()
    else:
      self.server_socket.listen(self.connlim)
    
    while True:
      zombie_socket, zombie_addr = self.server_socket.accept()
      # because we can't kill the accept thread, we will listen
      # for an 'ending' socket to stop accept more connections
      # (see more at stop_collecting) 
      if zombie_socket.recv(3).decode() == 'end':
        break
      # TODO: handle client disconnections
      self.zombies[zombie_addr] = zombie_socket
      print(f"[+] New connection established from {zombie_addr[0]}")


  """
  stop_collecting() stops accepting further connections to the server socket,
  it achieves that by sending a socket containing the data 'end' to signal
  collect_zombies() to stop accepting more connections.

  @params: None
  @return: None
  """
  def stop_collecting(self):
    # sending a "end of listening" signal to the server socket
    # in order to kill the last accept() thread
    t_socket = socket.socket()
    t_socket.connect((self.HOST, self.PORT))
    t_socket.send('end'.encode())
    t_socket.close()


  """
  start_cracking() is responsible for dividing the bruteforcing work equally between
  the zombies and for threaded communication between the host and each zombie to
  see if the hash as been cracked or not.

  @params:
    - wordlist_path(string), the path to the wordlist
    - md5_hash(string), the target MD5 hash to crack
  @return: None
  """
  def start_cracking(self, wordlist_path: str, md5_hash: str):
    if len(self.zombies) == 0:
      print("Not enough zombies were collected to start cracking (0)")
      sys.exit()

    # NOTE: assuming all words are newline-seperated.
    with open(wordlist_path, 'r') as file:
      words = [word.strip('\n') for word in file.readlines()]
      n = len(words)
      k = len(self.zombies)
      for i,j in enumerate(self.zombies):
        # i - ranging from 0..k
        # j - the key of each entry at dict self.zombies
        
        # divide the wordlist words equally between each client
        currSlice = words[math.floor(i/k*n):math.floor((i+1)/k*n)]
        conn = self.zombies[j]
        data = {
          "md5_hash": md5_hash,
          "wordlist": currSlice
        }
        # work in threads so we can listen for multiple responses from each zombie
        zcomm_thread = threading.Thread(target=self.communicate_zombie, args=(conn, j, data))
        zcomm_thread.start()

  
  """
  communicate_zombie() is responsible for sending the associated wordlist to each zombie
  and for checking if the zombie found a matching hash from it's given wordlist

  @params:
    - conn(socket.socket()), a zombie's socket
    - z_addr(tuple), the address of the zombie
    - data(dict), contains the md5 hash(string) and a wordlist(list[string])
  @return: None
  """
  def communicate_zombie(self, conn, z_addr, data):
    # send data to zombie(conn) as follows:
    # header(len of data str) + ';' + data
    msg = json.dumps(data)
    conn.send((str(len(msg))+';'+msg).encode())

    # listen for it's response
    response = ""
    while True:
      c = conn.recv(1).decode()
      if c == ';': break
      response += c

    # check for match
    if response.strip() != ";":
      print(f"[SUCC] {z_addr[0]} successfully cracked the hash: {response[response.find(';')+1:]}")
      return

    print(f"[!] {z_addr[0]} couldn't crack the hash")
    self.server_socket.close()
