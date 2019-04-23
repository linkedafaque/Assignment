# Assignment

Assignment to pipeline data from APIs into a database in order to be able to power graphs for reading various metrics associated with influencers such as their follower count, following count, follower ratio and others.

## Installation

MongoDB Installation 
After Installation, run **mongod** in one shell and **mongo** in the other.
```
brew update
brew install mongodb
mkdir -p /data/db
sudo chown -R `id -un` /data/db
```

Python Modules Installation (Python v3.5)
```
pip install pymongo
pip install requests
```
