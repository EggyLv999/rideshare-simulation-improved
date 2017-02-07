from pymongo import MongoClient
import pickle

def main():
	
	coll = MongoClient().db.taxi11
	agg = coll.aggregate([{'$sample': {'size': 40}}])
	i = 0
	for sample in agg:
		# print sample
		lat = sample['pickupLatitude']
		lon = sample['pickupLongitude']
		print lat
		print lon

		res = coll.find({
			'pickupLatitude': {
				'$gt': lat - 0.0003,
				'$lt': lat + 0.0003
			},
			'pickupLongitude': {
				'$gt': lon - 0.0003,
				'$lt': lon + 0.0003
			}
		})
		print res.count()
		if res.count() >= 10:
			file = open('data/dat{}'.format(i), 'w')
			l = []
			for r in res:
				l.append(r)
			pickle.dump(l, file)
			i += 1
			file.close()

if __name__ == '__main__':
	main()