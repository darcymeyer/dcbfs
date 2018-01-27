from Crypto.Hash import SHA512
from Crypto.Cipher import AES
import settings
import os

def hash_data(data):
	h = SHA512.new() # hashing algorithm subject to change
	h.update(data)
	return h.digest()

def encrypt_block(data, key, iv):
	# `data` is already padded
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	encrypted = encryptor.encrypt(data)
	return encrypted

def decrypt_block(data, key, iv):
	# `data` does not contain the header
	decryptor = AES.new(key, AES.MODE_CBC, iv)
	decrypted = decryptor.decrypt(data)
	return decrypted

# eventually this function should read directly from a file
def generate_block_content(content, blocksize=BLOCKSIZE):
	# `content` is the bytes of an unencrypted file
	content_length = len(content)
	counter = 0
	while counter < content_length:
		content_slice = content[counter:min(counter+blocksize, content_length)]
		block = content_slice + (blocksize-len(f)%blocksize)*'\x00'
		yield block
		counter += blocksize

def assemble_blocks(out_file, *args):
	# `outfile` is a filename string
	# `args` should be all the filenames of the individual blocks, in order
	with open(out_file, 'w') as of:
		for blockfile in args:
			with open(blockfile, 'r') as bf:
				of.write(bf.read())
			os.remove(blockfile)
