from pymongo import MongoClient
import pickle

def main():
	
	coll = MongoClient().db.taxi11
	agg = coll.aggregate([{'$sample': {'size': 500}}])
	i = 200
	for sample in agg:
		# print sample
		lat = sample['pickupLatitude']
		lon = sample['pickupLongitude']
		print lat
		print lon

		res = coll.find({
			'pickupLatitude': {
				'$gt': lat - 0.0001,
				'$lt': lat + 0.0001
			},
			'pickupLongitude': {
				'$gt': lon - 0.0001,
				'$lt': lon + 0.0001
			}
		})
		print res.count()
		if res.count() >= 10:
			file = open('data2/dat{}'.format(i), 'w')
			l = []
			bf = False
			for r in res:
				if r['pickupLatitude'] < 30 or r['pickupLongitude'] > -60 or r['dropoffLatitude'] < 30 or r['dropoffLongitude'] > -60:
					bf = True
					break
				l.append(r)
			if bf:
				print 'break'
				continue
			pickle.dump(l, file)
			i += 1
			file.close()

if __name__ == '__main__':
	main()