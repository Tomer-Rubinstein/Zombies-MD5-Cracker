from server import Server
import threading
import socket
import sys


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
	print(ASCII_ART)

	if len(sys.argv) != 2:
		print("[ERROR] Please enter port no. as the 2nd argument")
		sys.exit()

	PORT = int(sys.argv[1])
	server = Server(socket.gethostname(), PORT)
	server.init_server()

	collect_thread = threading.Thread(target=server.collect_zombies)
	collect_thread.start()

	print("Listening for connections..\nWhen ready, enter 'start' to start cracking, CTRL+C to abort")
	print("or 'zombies' to show connected zombies.\n")
	while True:
		try:
			user_input = input('$ ')
			if user_input == 'start':
				server.stop_collecting()
				server.start_cracking('wordlist.txt', '9ab6ff8d53822ff1dc8c12c9317f530c') # TODO: argparse
				break
			elif user_input == 'zombies':
				print(f"Currently, there are {len(server.zombies)} connected zombies:")
				print("".join(["\t@ "+ip_addr[0]+"\n" for ip_addr in server.zombies.keys()]))
		except KeyboardInterrupt:
			server.stop_collecting()
			sys.exit()


if __name__ == '__main__':
  main()
