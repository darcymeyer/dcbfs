from settings import *
from util import *
from file_ledger import PersonalFileLedger, GiantFileLedger
personal_ledger = PersonalFileLedger(DCBFS_MAIN_DIR)
giant_ledger = GiantFileLedger(DCBFS_MAIN_DIR, known_hosts=KNOWN_HOSTS)
from os import system

def get_space():
	size = system("du -h -d 0 "+DCBFS_MAIN_DIR+" | awk '{ print $1 }'")
	size = size.replace("K", "000")
	  .replace("M", "000000").replace("G", "000000000")
	 return int(size)

def backup_to_local():
	if get_space() >= MAX_STORAGE:
		return
	# on to the replication
	for bn, details in giant_ledger.ledger:
		if len(details['locations']) < REDUNDANCY:
			block = None
			for addr in details['locations']:
				try:
					block = get_remote_block(addr, bn)
				except:
					# should be courtious and update ledger. eventually.
					continue
			if block == None:
				raise Exception("[ERROR] Block {} could not be retrieved. \
				  It may be lost to the void.".format(bn))
			with open(STORAGE_DIR+bn) as f:
				f.write(bn)
			giant_ledger.add_location(bn, THIS_LOCATION)
			if get_space >= MAX_STORAGE:
				return
