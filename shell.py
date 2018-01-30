from settings import *
from datetime import datetime

def helptext():
	print('fields: 1-id_hash(64), 2-timestamp(4), 3-iv(16), 4-md5_hash(16), 5-content')
	print('n for new block, h for help, q for quit')

def human_readable(timestamp):
	epoch = int.from_bytes(timestamp, byteorder='big')
	hr = datetime.fromtimestamp(epoch)
	return hr.strftime('%Y-%m-%d %H:%M:%S')

def open_shell():
	while True:
		try:
			block_id = input('block id to examine: ')
			if block_id=='q':
				print("quitting")
				return
			with open(STORAGE_DIR+block_id, 'rb') as f:
				id_hash = f.read(64)
				timestamp = f.read(4)
				iv = f.read(16)
				md5_hash = f.read(16)
				content = f.read(BLOCKSIZE)
		except Exception as e:
			print("couldn't find block:", e)
			continue
		helptext()
		print('enter field number to examine:')
		while True:
			action = input('> ')
			if action=='1':
				print("id_hash:",id_hash)
			elif action=='2':
				print("timestamp:",timestamp, "=", human_readable(timestamp))
			elif action=='3':
				print("initialization vector:",iv)
			elif action=='4':
				print("md5 hash:",md5_hash)
			elif action=='5':
				print("content:",content)
			elif action=='h' or action=='help':
				helptext()
			elif action=='n':
				break
			elif action=='q':
				print("quitting")
				return
			else:
				print("invalid input")

if __name__=="__main__":
	open_shell()