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
	print(ASCII_ART)

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', type=int, required=False)
	parser.add_argument('--connlim', type=int, required=False)

	cli_args = parser.parse_args()
	PORT = cli_args.port
	CONNECTIONS_LIMIT = cli_args.connlim
	if not PORT:
		PORT = 3000

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
