from Crypto.Hash import SHA512, MD5
from Crypto.Cipher import AES
from settings import *
import os
from time import time
from binascii import hexlify
import re
import json
import pdb
from datetime import datetime
import struct

def block_examination_help_text():
	'''
	Prints help text for block examination.
	'''
	print('''fields
			------
			1-id_hash(64)
			2-timestamp(4)
			3-iv(16)
			4-md5_hash(16)
			5-content''')
	print('h for help or q for quit')

def hash_data(data):
	'''
	Hash data with SHA512
	'''
	h = SHA512.new() # hashing algorithm subject to change
	h.update(data.encode('utf-8'))
	return h.digest()

def checksum(data, c=None):
	'''
	Checksum with md5
	'''
	h = MD5.new()
	try:
		h.update(data.encode('utf-8'))
	except:
		h.update(data)
	if c and c!=h.digest():
		raise Exception('Checksum does not match data')
	return h.digest()

def encrypt_content(data, key, iv):
	'''
	Encrypt a pre-padded block of data, return it as is
	'''
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	encrypted = encryptor.encrypt(data)
	return encrypted

def decrypt_content(data, key, iv):
	'''
	Decrypt an encrypted block of data. Do not remove padding.
	`data` does not contain a header.
	'''
	decryptor = AES.new(key, AES.MODE_CBC, iv)
	decrypted = decryptor.decrypt(data)
	return decrypted

def generate_block_content(filepath, blocksize=BLOCKSIZE):
	'''
	Return the file's bytes in chunks in a generator
	'''
	padding_length = 0
	with open(filepath, 'rb') as f:
		while padding_length==0:
			content_slice = f.read(blocksize)
			padding_length = blocksize-(len(content_slice)-1)%blocksize-1
			block = content_slice + padding_length*b'\x00'
			# should really add a note within the block content of how many null bytes were added
			yield block

def timestamp():
	return int(time())

def timestamp_bytes():
	t = timestamp()#int(time())
	b = bytearray([0,0,0,0])
	b[3] = t & 0xFF
	t >>= 8
	b[2] = t & 0xFF
	t >>= 8
	b[1] = t & 0xFF
	t >>= 8
	b[0] = t & 0xFF
	return b

def make_block(filename, content, block_num, key):
	'''
	Take some data, encrypt it, add a header
	'''
	id_hash = hash_data(filename +"/"+ str(block_num))
	iv = os.urandom(16)
	block_content = encrypt_content(content, key, iv)
	md5 = checksum(block_content)
	block = id_hash + timestamp_bytes() + iv + md5 + block_content
	return block

def disassemble_block(block, block_num, key):
	'''
	Given a block, get its decrypted content
	'''
	# `block_num` is not currently used (?)
	iv = block[68:68+16]
	encrypted = block[100:]
	# checksum should already have been verified
	decrypted = decrypt_content(encrypted, key, iv)
	return decrypted

def get_remote_block(id_hash):
	'''
	Grab a single block, specified by `id_hash`
	'''
	blockname = hexlify(id_hash).decode('utf-8')
	if os.path.exists(STORAGE_DIR+blockname):
	#eventually this will query the giant ledger and grab the block from a remote machine
	# it should also check with the md5 checksum
		with open(STORAGE_DIR+blockname, 'rb') as f:
			block = f.read()
			return block
	else:
		# find the block on a remote machine
		for location in giant_ledger.get_block_locations(blockname):
			block = b''
			r = requests.get("http://"+location+"/storage/"+blockname, 
			  stream=True)
			with open(STORAGE_DIR+blockname) as f:
				for data in r.iter_content():
					block = block+data
					# https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python

def get_num_blocks(filename):
	'''
	Number of blocks over which file is stored
	'''
	with open(DCBFS_MAIN_DIR+"personal_ledger", 'r') as f:
		num = personal_ledger.ledger[filename][0]
		return int(num)

def human_readable(timestamp):
	'''
	Convert the bytes of the timesamp into human-readable string
	'''
	# epoch = int.from_bytes(timestamp, byteorder='big')
	epoch = struct.unpack(">i", timestamp)[0]
	hr = datetime.fromtimestamp(epoch)
	return hr.strftime('%Y-%m-%d %H:%M:%S')

def _explore():
	'''
	Display the uploaded files
	'''
	print('FILES')
	NUM_DASHES = 10
	print(''.join(['-' for x in range(NUM_DASHES)]))
	print('\n'.join(personal_ledger.list_files()))


def _examine_block(f):
	'''
	A shell function to view aspects of a block
	'''
	block_id = personal_ledger.get_id(f)
	try:
		if block_id == 'q':
			print "quitting"
			return
		with open(STORAGE_DIR+block_id, 'rb') as f:
			id_hash = f.read(64)
			timestamp = f.read(4)
			iv = f.read(16)
			md5_hash = f.read(16)
			content = f.read(BLOCKSIZE)
	except Exception as e:
		print "couldn't find block:", e
		return
	block_examination_help_text()
	print 'enter field number to examine:'
	while True:
		action = raw_input('> ')
		if action == '1':
			print"id_hash:", id_hash
		elif action == '2':
			print "timestamp:", human_readable(timestamp)
		elif action == '3':
			print "initialization vector:", iv
		elif action == '4':
			print "md5 hash:", md5_hash
		elif action == '5':
			print "content:", content
		elif action == 'h' or action == 'help':
			block_examination_help_text()
		elif action == 'q':
			print "quitting"
			return
		else:
			print "invalid input"

def _init():
	'''
	Initializes block on system

	1) Creates storage directory
	2) Creates personal personal ledger
		a) If it exists, it leaves it (To-Do: Check if syntax correct.)
		b) If it doesn't, create it with an empty dictionary.
	'''
	if not os.path.exists(TEMP_DIR):
		os.makedirs(TEMP_DIR)
	if not os.path.exists(STORAGE_DIR):
		os.makedirs(STORAGE_DIR)
	if not os.path.exists(OUT_DIR):
		os.makedirs(OUT_DIR)
	if not os.path.exists(DCBFS_MAIN_DIR+'personal_ledger'):
		f = open(DCBFS_MAIN_DIR+'personal_ledger', 'a')
		f.write('{}')
		f.close()
	if not os.path.exists(DCBFS_MAIN_DIR+'giant_ledger'):
		f = open(DCBFS_MAIN_DIR+'giant_ledger', 'a')
		f.write('{}')
		f.close()
	# personal_ledger.read() # not sure if this is needed
