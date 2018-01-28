from settings import *
from util import *
import time
import os
from binascii import hexlify

# note: initialization vector does not need to be secret

def upload_file(filepath):
	key = input('enter key:')
	with open(filepath, 'r') as f:
		raw_file = f.read()
	#eventually `filepath` should be passed directly to `generate_block_content`
	filename = os.path.basename(filepath)
	block_num = 0
	for block in generate_block_content(raw_file):
		id_hash = hash_data(filename +"/"+ str(block_num))
		# "/" or any character not allowed in a filename
		iv = os.urandom(16)
		block_content = encrypt_block(block, key, iv)
		md5 = checksum(block_content)
		total_block = (id_hash + timestamp() + iv + md5 + block_content)
		with open(STORAGE_DIR + hexlify(id_hash).decode('utf-8'), 'wb') as f:
		# i question whether this is too long of a filename
			f.write(total_block)
		block_num += 1
	#update_file_ledger('add', filename, block_num)