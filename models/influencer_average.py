
class InfluencerAverage:

	def __init__(self, pk, totalFollowerCount, totalFollowingCount, totalDataPoints, datetime):
		self.pk = pk
		self.totalFollowerCount = totalFollowerCount
		self.totalFollowingCount = totalFollowingCount
		self.totalDataPoints = totalDataPoints
		self.datetime = datetime

	def serialize(self):
		return {
			'pk': self.pk,
			'totalFollowerCount': self.totalFollowerCount,
			'totalFollowingCount': self.totalFollowingCount,
			'totalDataPoints': self.totalDataPoints,
			'averageFollowerCount': float((self.totalFollowerCount * 1.0) / self.totalDataPoints),
			'averageFollowingCount': float((self.totalFollowingCount * 1.0) / self.totalDataPoints),
			'datetime': self.datetime
		}
