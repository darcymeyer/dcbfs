###############################
# Note: must be run with sudo #
###############################

# create the filestructure
mkdir ~/.dcbfs
mkdir ~/.dcbfs/storage
mkdir ~/.dcbfs/out

# set up the daemon
mkdir /Library/dcbfs
mv manage /Library/dcbfs/
mv com.dcbfs.manager.plist /Library/LaunchDaemons
