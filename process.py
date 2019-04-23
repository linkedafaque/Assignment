import json
import time
import pymongo
import requests as rq
import multiprocessing as mp
from datetime import datetime

from models.influencer_average import InfluencerAverage
from models.influencer_stat import InfluencerStat
from db import get_config

START = 1000000
END = 1004000

results = []
followerCounts = {}
followingCount = {}
totalDataPoints = {}

config = get_config('mongo')

API = config['endpoint']
client = pymongo.MongoClient(config['host'])
db = client[config['db']]
stats_collection = db[config['statscollection']]
averages_collection = db[config['averagescollection']]

"""
Hits Influencer API and gets all the data
"""
def getInfluencerStat(pk):
	try:
		endpoint = API + str(pk)
		response = rq.get(endpoint)
		response = json.loads(response.content.decode('utf-8'))
		influencerStat = InfluencerStat(response['pk'], response['username'], response['followerCount'], response['followingCount'])
		return influencerStat
	except Exception as e:
		print(e)


"""
Collects all the data and stores them in a list
Also, the followerCount, followingCount and totalDataPoints is stored 
to be able to sum up and compute averages later
"""
def collect_result(result):
	followerCounts[result.getPK()] = result.getfollowerCount()
	followingCount[result.getPK()] = result.getFollowingCount()
	totalDataPoints[result.getPK()] = 1
	results.append(result.serialize())


"""
Gets All the current averages of influencers stored in DB
and computes the new averages by adding the new statistics
"""
def getUpdatedAveragesOfInfluencers():
	records =  averages_collection.find({"pk": {"$gte": START, "$lte": END}})
	for record in records:
		followerCounts[record['pk']] += record['totalFollowerCount']
		followingCount[record['pk']] += record['totalFollowingCount']
		totalDataPoints[record['pk']] += record['totalDataPoints']


"""
Updates the new averages in the averages collection
"""
def updateAverages():
	for result in results: 
		influencerAverage = InfluencerAverage(result['pk'], followerCounts[result['pk']], followingCount[result['pk']],
			totalDataPoints[result['pk']], result['datetime'])
		query = { 'pk': result['pk'] }
		update = influencerAverage.serialize()
		averages_collection.update(query, update, upsert=True)


print("Started Fetching Data From APIs")
starttime = time.time()
pool = mp.Pool(mp.cpu_count())


"""
Used multiprocessing library to be able to execute the function hitting APIs in a 
concurrent fashion and speed up the gathering of influencer statistics
"""
for pk in range(START, END):
	pool.apply_async(getInfluencerStat, args=(pk,), callback=collect_result)

pool.close()
pool.join()

print('Completed Fetching Results From APIs In: ' + str(time.time() - starttime) + ' seconds')
stats_collection.insert_many(results)

getUpdatedAveragesOfInfluencers()
updateAverages()

print('Total Time Taken: ' + str(time.time() - starttime) + ' seconds')
