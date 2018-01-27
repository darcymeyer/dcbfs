# settings for where to store and access files

DCBFS_MAIN_DIR = '~/.dcbfs/'
TEMP_DIR = DCBFS_MAIN_DIR + 'temp/'
STORAGE_DIR = DCBFS_MAIN_DIR + 'storage/'
GIANT_LEDGER_FILE = DCBFS_MAIN_DIR + 'giant_ledger'
BLOCKSIZE = 256 # 256 bytes; will be much larger after testing phase
# BLOCKSIZE must be a multiple of 16, and its unit is bytes