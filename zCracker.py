from server import Server
import threading
import socket
import sys
import argparse

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

def main():
  parser = argparse.ArgumentParser(description="zCracker is a multi-client threaded server software to decode a MD5 hash using a botnet.\nSource: https://github.com/Tomer-Rubinstein/Zombies-MD5-Cracker")
  parser.add_argument('--port', type=int, required=False, help="port to bind the server to")
  parser.add_argument('--connlim', type=int, required=False, help="limit the no. of zombies in the botnet")
  parser.add_argument('--hash', type=str, required=True, help="target MD5 Hash to decrypt")
  parser.add_argument('--wordlist', type=str, required=True, help="path to a wordlist file with words seperated by newlines")

  cli_args = parser.parse_args()
  PORT = cli_args.port
  CONNECTIONS_LIMIT = cli_args.connlim
  HASH = cli_args.hash
  WORDLIST = cli_args.wordlist
  if not PORT:
    PORT = 3000

  print(ASCII_ART)
  server = Server(socket.gethostname(), PORT, CONNECTIONS_LIMIT)
  server.init_server()

  collect_thread = threading.Thread(target=server.collect_zombies)
  collect_thread.start()

  print(f"Listening for connections on port {PORT}..\nWhen ready, enter 'start' to start cracking, CTRL+C to abort")
  print("or 'zombies' to show connected zombies.\n")
  while True:
    try:
      user_input = input('$ ')
      if user_input == 'start':
        server.stop_collecting()
        server.start_cracking(WORDLIST, HASH)
        break
      elif user_input == 'zombies':
        print(f"Currently, there are {len(server.zombies)} connected zombies:")
        print("".join(["\t@ "+ip_addr[0]+"\n" for ip_addr in server.zombies.keys()]))
    except KeyboardInterrupt:
      server.stop_collecting()
      sys.exit()


if __name__ == '__main__':
  main()
