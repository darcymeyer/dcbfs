from dcbfs.settings import *
from dcbfs.util import *
import time
import os
from binascii import hexlify
import hashlib
import click
# note: initialization vector does not need to be secret

def upload_file(filepath, password):
	"""
	Uploads a file to a local repo.

	# TODO: add to the giant ledger
	"""
	key = hashlib.sha256(password.encode()).digest()
	filename = os.path.basename(filepath)
	block_num = 0
	for content in generate_block_content(filepath):
		block = make_block(filename, content, block_num, key)
		with open(STORAGE_DIR + hexlify(block[:64]).decode('utf-8'), 'wb') as f:
		# i question whether this is too long of a filename
			f.write(block)
		block_num += 1
	access_file_ledger('add', filename, block_num)

def recreate_file(filename):
	num_blocks = get_num_blocks(filename)
	with open(OUT_DIR + filename, 'ab+') as f:
		password = input('Enter password: ')
		key = hashlib.sha256(password.encode()).digest()
		block_num = 0
		while block_num < num_blocks:
			id_hash = hash_data(filename+"/"+str(block_num))
			# this is a terrible id. the hash should include a nonce or something (to be stored in personal ledger)
			block = get_remote_block(id_hash)
			content = disassemble_block(block, block_num, key)
			f.write(content)
			block_num += 1
	# access_file_ledger('remove', filename, block_num)

def delete_file(filename):
	access_file_ledger('remove', filename, block_num)
	# TODO: release revocation statements
