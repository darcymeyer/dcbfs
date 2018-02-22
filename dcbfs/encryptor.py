from settings import *
from util import *
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
	filename = os.path.basename(filepath).encode("ascii", "ignore")
	# print "filename: "+filename
	# print type(filename)
	block_num = 0
	fn = None
	for content in generate_block_content(filepath):
		block = make_block(filename, content, block_num, key)
		fn = hexlify(block[:64]).decode('utf-8')
		with open(STORAGE_DIR + fn, 'wb') as f:
			# i question whether this is too long of a filename
			# i question whether making the filename part of the data is necessary.
			# Also. If it has the same name, but different data, this fails.
			f.write(block)
		block_num += 1
	personal_ledger.add(filename, block_num, fn)

def recreate_file(filename, pw):
	num_blocks = get_num_blocks(filename)
	with open(OUT_DIR + filename, 'ab+') as f:
		password = pw#raw_input('Enter password: ')
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
	personal_ledger.remove(filename, block_num)
	# TODO: release revocation statements
