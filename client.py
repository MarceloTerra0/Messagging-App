import socket
import PySimpleGUI as sg
import threading
import time
import sys

def send(msg,flag):
	if msg == "":
		sg.popup_no_wait('The message was not sent')
	elif msg == DISCONNECT_MESSAGE and not flag:
		sg.popup_no_wait('Exit the application to disconnect')
	elif len(msg) > 300:
		 sg.popup_no_wait('Keep the message under 300 characters')
	else:
		message = USERNAME.encode(FORMAT) + ' - '.encode(FORMAT) + msg.encode(FORMAT)
		msg_length = len(message)
		send_length = str(msg_length).encode(FORMAT)
		send_length += b' ' * (HEADER - len(send_length))
		client.send(send_length)
		client.send(message)


def recieve():
	global messages
	global recieved
	global running
	while running:
		try:
			msg_length = client.recv(HEADER).decode(FORMAT)
			if msg_length:
				msg_length = int(msg_length)
				msg = client.recv(msg_length).decode(FORMAT)
				messages += msg + '\n\n'
				recieved = 1
		except:
			if not running:
				print("Not running ",running)
	print("Teste!")

def refresh_window():
	window['output'].update(value='')
	print(messages)


HEADER = 4
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
recieved = 0
messages = ''
running = True
USERNAME = ''
SERVER = ''
invalid = False

layout = [
			[sg.Text('Messenger',size=(0,0),key='title')],
			[sg.Input(size=(30,0),key='message')],
			[sg.Button('Send message',key='send')],
			[sg.Output(size=(80,30),key='output')]
		]

layout_popup = [
			[sg.Text('Username',size=(0,0)),sg.Input(size=(30,0),key='username')],
			[sg.Text('IP address',size=(0,0)),sg.Input(size=(30,0),key='ipaddr')],
			[sg.Button('Next',key='next')]
		]

layout_invalid_values = [
			[sg.Text('Invalid values!')]
		]

if __name__ == '__main__':
	user_input = sg.Window("Messenger").layout(layout_popup)
	invalid = True

	while True:
		event, values = user_input.read()

		if event in (None, 'Exit'):
			invalid = True
			break

		if event in ('next'):
			USERNAME = values.get('username')
			SERVER = values.get('ipaddr') 
			if not USERNAME or not SERVER:
				sg.PopupQuick('Invalid values!', auto_close=False)
			elif len(USERNAME) > 13:
				sg.PopupQuick('Keep your username under 13 characters', auto_close=False)
			else:
				invalid = False
				break

	if not invalid:
		user_input.close()
		ADDR = (SERVER, PORT)
		CLIENT_IP_ADDRESS = socket.gethostbyname(socket.gethostname())
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)

		window = sg.Window("Messenger").layout(layout)
		client.settimeout(2)
		thread = threading.Thread(target=recieve, args=())
		thread.start()

		while True:
			event, values = window.read(timeout=1)

			if event in (None, 'Exit'):
				send(DISCONNECT_MESSAGE,'disc')
				running = False
				while threading.activeCount() - 1 > 0:
					time.sleep(0.5)
				break
			
			if event in ('send',):
				send(values.get('message'),'')
				window['message'].update(value='')
				window['output'].update(value='')
				print(messages)

			if recieved == 1:
				refresh_window()
				recieved = 0

	sys.exit()
