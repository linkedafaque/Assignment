import pymongo
import requests as rq
import json
import multiprocessing as mp
import time
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


def getInfluencerStat(pk):
	try:
		endpoint = API + str(pk)
		response = rq.get(endpoint)
		response = json.loads(response.content.decode('utf-8'))
		influencerStat = InfluencerStat(response['pk'], response['username'], response['followerCount'], response['followingCount'])
		return influencerStat
	except Exception as e:
		print(e)


def collect_result(result):
	followerCounts[result.getPK()] = result.getfollowerCount()
	followingCount[result.getPK()] = result.getFollowingCount()
	totalDataPoints[result.getPK()] = 1
	results.append(result.serialize())


def getUpdatedAveragesOfInfluencers():
	records =  averages_collection.find({"pk": {"$gte": START, "$lte": END}})
	for record in records:
		followerCounts[record['pk']] += record['totalFollowerCount']
		followingCount[record['pk']] += record['totalFollowingCount']
		totalDataPoints[record['pk']] += record['totalDataPoints']


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

for pk in range(START, END):
	pool.apply_async(getInfluencerStat, args=(pk,), callback=collect_result)

pool.close()
pool.join()

print('Completed Fetching Results From APIs In: ' + str(time.time() - starttime) + ' seconds')
stats_collection.insert_many(results)

getUpdatedAveragesOfInfluencers()
updateAverages()

print('Total Time Taken: ' + str(time.time() - starttime) + ' seconds')




