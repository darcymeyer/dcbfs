# Decentralized Cloud-Based File Storage

## Encryption

AES, CBC. (If someone wants to argue for different encryption, please do.)

## Ledgers

### Giant Ledger

Contains id, location, timestamp of each block, and revocation statements.

**MUST FIGURE OUT A WAY TO ISSUE A CRYPTOGRAPHICALLY SECURE REVOCATION STATEMENT FOR A BLOCK (THAT IS ALSO NOT ABLE TO BE RELATED TO OTHER BLOCKS IN THE SAME FILE)**

Also, would this be too big?

### Individual File Ledger

Contains the ids of the blocks that form the original file, their order, and the keys with which to decrypt them. Its own id is a hash of the filename and the publisher name.

### Personal Ledger

Each publisher has one personal ledger. Its id is a hash of the publisher's secret, and is encrypted with that secret. It is padded to the standard block size. Every time a publisher uploads a file, their personal ledger block is revoked and a new one is added to the giant ledger (blocks don't do updates; they are only created or deleted).

## Individual Blocks

Each block has padding added to it so they are all the same size. They will have headers which contain the timestamp of when they were last checked and a hash of their id. Blocks are stored on individual machines.

**Header:** 116 bytes: 64 bytes for a sha512 hash of some identifying information, 4 bytes for a timestamp (unix epoch time), 16 bytes for the initialization vector, 32 bytes for a md5 hash of the content (used as checksum)

## Rules for computers participating in the scheme

**Giant Ledger Maintenance:** Computers look at the ledger to check for the existence of block copies, and see which blocks should be copied or deleted. It checks the recorded locations of each block with a slightly old timestamp and updates the ledger if the block is not present in a location. If a block has too few copies or not enough availability (compute an availability score?), it copies it onto itself (if it has space) with a timestamp and records this on the ledger. If a block has been marked as revoked, and the computer finds it on itself, it deletes it from itself (and records this on the ledger).

**Uploading files:** Files are encrypted locally, then split up into standard-sized chunks (with padding if necessary), and each block receives a header (see [Individual Blocks](#individual-blocks)). The order of the blocks' ids are recorded in another block (that is indistinguishable from file blocks), and the id of *that* block is recorded in the user's personal ledger (that also looks like a file block).

**Deleting files:** For a use to delete a file, it issues a revocation statement for all the blocks of the file and the individual file ledger onto the giant ledger. 

**Local Maintenance:** If a computer finds a block on itself with a really old timestamp, it is deleted.
