from pymongo import MongoClient
import pickle

filename = 'data1.txt'

def main():
	file = open(filename, 'w')
	coll = MongoClient().db.taxi11
	res = coll.find({
		'pickupLatitude': {
			'$gt': 40.771,
			'$lt': 40.772
		},
		'pickupLongitude': {
			'$gt': -73.95,
			'$lt': -73.94
		}
	})
	print res.count()
	l = []
	for r in res:
		l.append(r)
	pickle.dump(l, file)
	file.close()

if __name__ == '__main__':
	main()