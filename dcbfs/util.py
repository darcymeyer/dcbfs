from Crypto.Hash import SHA512, MD5
from Crypto.Cipher import AES
from dcbfs.settings import *
import os
from time import time
from binascii import hexlify
import re

def hash_data(data):
	h = SHA512.new() # hashing algorithm subject to change
	h.update(data.encode('utf-8'))
	return h.digest()

def checksum(data, c=None):
	h = MD5.new()
	try:
		h.update(data.encode('utf-8'))
	except:
		h.update(data)
	if c and c!=h.digest():
		raise Exception('Checksum does not match data')
	return h.digest()

def encrypt_content(data, key, iv):
	# `data` is already padded
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	encrypted = encryptor.encrypt(data)
	return encrypted

def decrypt_content(data, key, iv):
	# `data` does not contain the header
	decryptor = AES.new(key, AES.MODE_CBC, iv)
	decrypted = decryptor.decrypt(data)
	return decrypted

def generate_block_content(filepath, blocksize=BLOCKSIZE):
	# just reads out the file and chunks it
	padding_length = 0
	with open(filepath, 'rb') as f:
		while padding_length==0:
			content_slice = f.read(blocksize)
			padding_length = blocksize-(len(content_slice)-1)%blocksize-1
			block = content_slice + padding_length*b'\x00'
			# should really add a note within the block content of how many null bytes were added
			yield block

def assemble_content(out_file, *args):
	# `outfile` is a filename string
	# `args` should be all the filenames of the individual blocks, in order
	with open(out_file, 'w') as of:
		for blockfile in args:
			with open(blockfile, 'r') as bf:
				of.write(bf.read())
			os.remove(blockfile)

def access_file_ledger(action, filename, num_blocks):
	with open(DCBFS_MAIN_DIR+"personal_ledger", 'r') as f: # don't hardcode this
		ledger = f.read()
	with open(DCBFS_MAIN_DIR+"personal_ledger", 'w') as f:
		if action=='add':
			ledger += filename+' : '+str(num_blocks)+'\n'
			f.write(ledger)
		elif action=='remove':
			ledger = re.sub(filename+' : '+str(num_blocks)+'\n', '', ledger)
			f.write(ledger)

def timestamp():
	t = int(time())
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
	id_hash = hash_data(filename +"/"+ str(block_num))
	iv = os.urandom(16)
	block_content = encrypt_content(content, key, iv)
	md5 = checksum(block_content) # leave this line alone!
	block = id_hash + timestamp() + iv + md5 + block_content
	return block

def disassemble_block(block, block_num, key):
	# `block_num` is not currently used (?)
	iv = block[68:68+16]
	encrypted = block[100:]
	# checksum should already have been verified
	decrypted = decrypt_content(encrypted, key, iv)
	return decrypted

def get_remote_block(id_hash):
	#eventually this will query the giant ledger and grab the block from a remote machine
	# it should also check with the md5 checksum
	blockname = hexlify(id_hash).decode('utf-8')
	with open(STORAGE_DIR+blockname, 'rb') as f:
		block = f.read()
		return block

def get_num_blocks(filename):
	with open(DCBFS_MAIN_DIR+"personal_ledger", 'r') as f:
		ledger = f.read()
		num = re.match('(?:'+filename+' : )([0-9]+)', ledger).group(1)
		return int(num)
