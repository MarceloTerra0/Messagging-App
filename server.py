import socket
import threading
import time
import PySimpleGUI as sg

HEADER = 4
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
lastSentMessage = ['Server - Hello, World!', '0', 0]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
	global lastSentMessage
	print(f"[NEW CONNECTION] {addr} connected.")
	lastRecievedMessage = ['abc', '0', time.time()]
	connected = True
	while connected:
		if lastRecievedMessage[2] != lastSentMessage[2]:
			lastRecievedMessage = lastSentMessage
			msg = lastSentMessage[0]
			message = msg.encode(FORMAT)
			msg_length = len(message)
			send_length = str(msg_length).encode(FORMAT)
			send_length += b' ' * (HEADER - len(send_length))
			conn.send(send_length)
			conn.send(message)

		conn.settimeout(0.5)
		try:
			msg_length = conn.recv(HEADER).decode(FORMAT)
			if msg_length:
				conn.settimeout(None)
				msg_length_original = msg_length.encode(FORMAT)
				msg_length = int(msg_length)
				msg = conn.recv(msg_length).decode(FORMAT)
				if DISCONNECT_MESSAGE in msg:
					connected = False
					print(f"[{addr}] has disconnected.")
					user = msg.split(' - ')
					print(user)
					lastSentMessage = (f'{user[0]} - has disconnected from the chat','0',time.time())
					time.sleep(5)
				else:
					print(f"[{addr}] Sent - {msg}")
					lastSentMessage = (msg, addr,time.time())
		except:
			pass
	conn.close()

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == '__main__':	
	print(f"[STARTING] server is starting... on IP: {SERVER}")
	start()