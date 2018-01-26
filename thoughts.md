## Thoughts

This is a system where files are encrypted and uploaded in pieces to a decentralized hive of internet-connected machines, where they are accessible at any time from any other machine that has the correct encryption key.

Each file will have to have a unique identifier, which will be a combination of the publisher's username and the filename. Each filename will be associated with a ledger which describes where each chunk of it is stored, since it will most likely have many copies of each chunk stored across multiple machines.

To upload a file, it will be encrypted with the key associated with the publisher, and then split into several chunks. A header will be attached to each chunk containing some kind of hash of the file name. Then each chunk will be copied to several machines in the hive that have set aside space to store files in exchange for uploading their own files. (The tradeoff is storage space for accessibility across machines.) A ledger will be created that records where each piece of the file is stored. Another part of the process will be that computers periodically review each file's ledger to check that several copies of each chunk are available, and create more copies of a chunk and then update the ledger if necessary. Each individual ledger could possibly be blockchain-based. To delete a file, the original publisher will release a revocation statement (similar to revoking a pubkey?) and the chunks will gradually be deleted. Every time a computer verifies the integrity of a file by checking for the chunks, it leaves a timestamp on the chunk to say so. If a chunk is not verified for a long period of time, it can be deleted (this ensures that dead chunks aren't left over if the ledger is deleted).


~~This could go in two ways. There could be a "master ledger" of ledgers, where each ledger would be for either one user or one file. But in order for all computers to maintain all files, every computer needs to be able to access a ledger where the locations of each block are recorded. Such a scheme would necessitate that each block have an id from which the filename could not be extracted. So an individual file's ledger would have to be secret. The blocks could not be split publicly by file. So this first way wouldn't work.~~

Or, there could be one giant ledger that contains all the locations of the blocks~~, and a separate ledger that contains encrypted ledgers each one for an individual file~~. One way to go would be to have each ledger be encrypted and stored like a block, so it would be in the giant ledger. Then a user would have to be able to differentiate their own ledgers from the rest using only a single secret. You could have one ledger per file, and then one user's file ledgers would have to not be able to be related to each other. This might require adding other different secrets to hashes, and those additional secrets would have to be stored in a single encrypted block on the giant ledger, uniquely identified by a hash of the original secret or something [this is what we're going to do]. Another way, which skips an intermediate step, would be to have each ledger be a ledger of the user, and all files' blocks are recorded on it, and it would be uniquely identifiable from the original single secret. 

~~The possibility of having one ledger for blocks and one ledger for ledgers would make the ledgers more attackable. (Question: how much information in a ledger for one file will there actually need to be?)~~ There is only one ledger

We should definitely separate the information of which blocks belong to which files in which order from the number and locations of each block. This necessitates the giant ledger with all the blocks. [all good]

**Users still need the ability to revoke blocks to stop being copied and be deleted. If all machines are duplicating blocks based on the giant ledger, that is where the information would need to be available about no longer duplicating a block. There would also have to be a cryptographic relationship between the publisher of a block and the block, so people don't try to delete each other's blocks.**

**How does one know they have a correct copy of the ledger (blockchain)? While still having the ability to delete all traces of a file? Would the back end of the blockchain gradually delete itself (but then we might loose the ability to resolve forks)?**

Since everything is stored on someone else's computer, ideally ledgers should be indistinguishable from blocks. [all good]

So the decision is between having a user's secret lead directly to one block containing all the info for all the files, or leading to one block that contains the info for each ledger for each file, and those ledgers are also different blocks. [second option]

~~How do you find your starting block among so many other blocks?~~ Its name is derived from the publisher's secret.

**NOTE: salt things**