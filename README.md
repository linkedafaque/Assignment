# Assignment

Assignment to pipeline data from APIs into a database in order to be able to power graphs for reading various metrics associated with influencers such as their follower count, following count, follower ratio and others.

## Flow Diagram

![Flow Diagram](https://github.com/linkedafaque/Assignment/blob/master/FlowDiagram.png)

## Modules Used

Python Multiprocessing Library has been used in order to take advantage of the cores of the CPU wherein the API hitting task is sent to each of the cores available with a subset of the total influencers available and executed concurrently. Separate subsets are run of separate cores.

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
