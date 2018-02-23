from settings import *
from file_ledger import PersonalFileLedger, GiantFileLedger
from util import *
import time
import os
from binascii import hexlify
import hashlib
import click

# note: initialization vector does not need to be secret

personal_ledger = PersonalFileLedger(DCBFS_MAIN_DIR)
giant_ledger = GiantFileLedger(DCBFS_MAIN_DIR, known_hosts=KNOWN_HOSTS)

def upload_file(filepath, password):
	'''
	Upload a file.
	Currently only works with a local repo.
	'''
	key = hashlib.sha256(password.encode()).digest() # length 32
	filename = os.path.basename(filepath).encode("ascii", "ignore")
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
	# TODO: add to the giant ledger

def recreate_file(filename, password):
	'''
	Retrieve a file.
	Currently only works with local repo.
	'''
	num_blocks = get_num_blocks(filename)
	with open(OUT_DIR + filename, 'ab+') as f:
		key = hashlib.sha256(password.encode()).digest()
		block_num = 0
		while block_num < num_blocks:
			id_hash = hash_data(filename+"/"+str(block_num))
			# this is a terrible id. the hash should include a nonce or something (to be stored in personal ledger)
			block = get_remote_block(id_hash)
			content = disassemble_block(block, block_num, key)
			f.write(content)
			block_num += 1

def delete_file(filename):
	'''
	Delete a file.
	Currently only works with local repo.
	'''
	personal_ledger.remove(filename, block_num)
	# TODO: release revocation statements
