from Crypto.Hash import SHA512, MD5
from Crypto.Cipher import AES
from settings import *
import os
from time import time
from binascii import hexlify

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
	print("encrypting: ", data, len(data), ", key/iv: ", key, iv)
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	encrypted = encryptor.encrypt(data)
	return encrypted

def decrypt_content(data, key, iv):
	# `data` does not contain the header
	print("decrypt_content: ", data, len(data), ", key/iv: ", key, iv)
	decryptor = AES.new(key, AES.MODE_CBC, iv)
	decrypted = decryptor.decrypt(data)
	return decrypted

# eventually this function should read directly from a file
def generate_block_content(content, blocksize=BLOCKSIZE):
	# `content` is the bytes of an unencrypted file
	content_length = len(content)
	print("gen block content: length", content_length)
	counter = 0
	while counter < content_length:
		content_slice = content[counter:min(counter+blocksize, content_length)]
		block = content_slice + (blocksize-(len(content_slice)-1)%blocksize-1)*'\x00'
		print("slice len:", len(content_slice), "block len:", len(block))
		yield block
		counter += blocksize

def assemble_content(out_file, *args):
	# `outfile` is a filename string
	# `args` should be all the filenames of the individual blocks, in order
	with open(out_file, 'w') as of:
		for blockfile in args:
			with open(blockfile, 'r') as bf:
				of.write(bf.read())
			os.remove(blockfile)

def update_file_ledger(action, filename, num_blocks):
	# open ledger

	# update ledger
	if action=='add':
		pass
	elif action=='remove':
		pass

	# close ledger


def timestamp():
	t = int(time())
	b = bytearray([0,0,0,0])
	b[3] = t & 0xFF
	t >>= 8
	b[2] = t & 0xFF
	t >>= 8
	b[1] = t & 0xFF
	t >>= 8
	b[0] = t & 0xF0
	return b

def make_block(filename, content, block_num, key):
	id_hash = hash_data(filename +"/"+ str(block_num))
	iv = os.urandom(16)
	block_content = encrypt_content(content, key, iv)
	md5 = checksum(block_content) # leave this line alone!
	block = id_hash + timestamp() + iv + md5 + block_content
	print("in make_block: id_hash", len(id_hash), "timestamp:", len(timestamp()), "iv", len(iv), "md5", len(md5), "block_content", len(block_content))
	return block

def disassemble_block(block, block_num, key):
	# `block_num` is not currently used (?)
	iv = block[68:68+16]
	encrypted = block[100:]
	print("in disassemble_block, block is:", block)
	print("in disassemble_block, encrypted is:", encrypted)
	# checksum should already have been verified
	decrypted = decrypt_content(encrypted, key, iv)
	print("disassemble block returning:", decrypted)
	return decrypted

def get_remote_block(id_hash):
	#eventually this will query the giant ledger and grab the block from a remote machine
	blockname = hexlify(id_hash).decode('utf-8')
	print("get rem block name is:", blockname)
	with open(STORAGE_DIR+blockname, 'rb') as f:
		print("reading from:", STORAGE_DIR+blockname)
		block = f.read()
		print("get_remote_block return:", block)
		return block
