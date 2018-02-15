import os
import json
from dcbfs.util import _init

class PersonalFileLedger():
	'''
	Represents the file ledger in memory
	'''
	def __init__(self, DCBFS_MAIN_DIR):
		self.fp = DCBFS_MAIN_DIR+"personal_ledger"
		if not os.path.exists(self.fp):
		    _init()
		self.read()


	def list_files(self):
		return list(self.ledger.keys())

	def get_id(self, fname):
		return self.ledger[fname]

	def add(self, filename, num_blocks, fn):
		'''
		Add a filename to the personal ledger
		'''
		assert type(filename) is str, 'Filename must be a string'
		self.ledger[filename] = (str(num_blocks), fn)

	def remove(self, filename):
		'''
		Removes a filename from the personal ledger
		'''
		assert type(filename) is str, 'Filename must be a string'
		del self.ledger[filename]

	def read(self):
		'''
		Reads from the personal ledger
		'''
		f = open(self.fp, 'r')
		self.ledger = json.load(f)
		f.close()

	def write(self):
		'''
		Writes the personal ledger
		'''
		output_f = open(self.fp, 'w')
		output_f.write(json.dumps(self.ledger, sort_keys=True))
		output_f.close()


class GiantFileLedger():
	'''
	To-Do: Implement as per Darcy's instruction
	'''
	pass