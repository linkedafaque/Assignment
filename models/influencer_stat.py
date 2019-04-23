
from datetime import datetime

class InfluencerStat:

	def __init__(self, pk, username, followerCount, followingCount):
		self.pk = pk
		self.username = username
		self.followerCount = followerCount
		self.followingCount = followingCount
		self.datetime = datetime.utcnow()

	def serialize(self):
		return {
			'pk': self.pk,
			'username': self.username,
			'followerCount': self.followerCount,
			'followingCount': self.followingCount,
			'followerRatio': float((self.followerCount * 1.0) / self.followingCount),
			'datetime': self.datetime
		}

	def getPK(self):
		return self.pk

	def getUsername(self):
		return self.username

	def getfollowerCount(self):
		return self.followerCount

	def getFollowingCount(self):
		return self.followingCount

	def getDateTime(self):
		return self.datetime


