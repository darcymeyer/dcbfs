from Crypto.Hash import SHA512

def hash_data(data):
	h = SHA512.new()
	h.update(data)
	returh h.digest()