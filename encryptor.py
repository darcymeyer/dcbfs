from settings import *
from util import *
import time
import os
from binascii import hexlify

# note: initialization vector does not need to be secret

def upload_file(filepath):
	key = input('enter key:')
	filename = os.path.basename(filepath)
	block_num = 0
	for content in generate_block_content(filepath):
		block = make_block(filename, content, block_num, key)
		with open(STORAGE_DIR + hexlify(block[:64]).decode('utf-8'), 'wb') as f:
		# i question whether this is too long of a filename
			f.write(block)
		print("block", block_num, "name:", hexlify(block[:64]).decode('utf-8'), "bytes:", block)
		block_num += 1
	access_file_ledger('add', filename, block_num)
	# TODO: add to the giant ledger

def recreate_file(filename):
	num_blocks = get_num_blocks(filename)
	with open(OUT_DIR + filename, 'ab+') as f:
		key = input('enter key:')
		block_num = 0
		while block_num < num_blocks:
			id_hash = hash_data(filename+"/"+str(block_num))
			block = get_remote_block(id_hash)
			content = disassemble_block(block, block_num, key)
			f.write(content)
			block_num += 1
	# access_file_ledger('remove', filename, block_num)

def delete_file(filename):
	access_file_ledger('remove', filename, block_num)
	# TODO: release revocation statements
