# Assignment

Assignment to pipeline data from APIs into a database in order to be able to power graphs for reading various metrics associated with influencers such as their follower count, following count, follower ratio and others.

## Flow

![Flow Diagram] (/Assignment/blob/master/FlowDiagram.png)

## Installation

MongoDB Installation. After Installation, run **mongod** in one shell and **mongo** in the other.
```
brew update
brew install mongodb
mkdir -p /data/db
sudo chown -R `id -un` /data/db
```

Create Database & Collections in Mongo Shell.
```
use influencerstat;
db.createCollection(“averages”);
db.createCollection(“stats”);
```

Python Modules Installation (Python v3.5).
```
pip install pymongo
pip install requests
```

Run process file to start pipelining data.
```
python process.py
```
