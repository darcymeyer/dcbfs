import os
import json
import pdb

class PersonalFileLedger():
	'''
	Represents the file ledger in memory
	'''
	def __init__(self, md):
		self.fp = md+"personal_ledger"
		if os.path.exists(self.fp):
			self.read()
		else:
			print('WARNING! Personal ledger doesn\'t exist! Try running `dcbfs init`.')

	def list_files(self):
		return list(self.ledger.keys())

	def get_id(self, fname):
		'''
		Get the storage id of a file
		'''
		try:
			return self.ledger[fname][1]
		except:
			raise ValueError("File: " + str(fname)+" does not exist!!!")

	def get_block(self, fname):
		'''
		Get the number of blocks over which a file is stored
		'''
		try:
			return self.ledger[fname][0]
		except:
			raise ValueError("File: " + str(fname)+" does not exist!!!")

	def add(self, filename, num_blocks, fn):
		'''
		Add an entry to the personal ledger
		'''
		assert type(filename) is str, 'Filename must be a string'
		self.ledger[filename] = (str(num_blocks), fn)
		self.write()

	def remove(self, filename):
		'''
		Remove a filename from the personal ledger
		'''
		assert type(filename) is str, 'Filename must be a string'
		del self.ledger[filename]
		self.write()

	def read(self):
		'''
		Load personal ledger into memory
		'''
		f = open(self.fp, 'r')
		self.ledger = json.load(f)
		f.close()

	def write(self):
		'''
		Write the personal ledger to file
		'''
		output_f = open(self.fp, 'w')
		output_f.write(json.dumps(self.ledger, sort_keys=True))
		output_f.close()

# personal_ledger = PersonalFileLedger(DCBFS_MAIN_DIR)

class GiantFileLedger():
	'''
	To-Do: Implement as per Darcy's instruction
	'''
	pass
