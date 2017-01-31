from datetime import datetime
from pymongo import MongoClient

def main():
	coll = MongoClient().db.taxi11
	file = open('../yellow_tripdata_2016-01.csv', 'r')
	print file.readline()
	count = 0
	total = 0
	dbobjs = []
	for line in file:
		params = line.split(',')
		a=datetime.strptime(params[1],'%Y-%m-%d %H:%M:%S')
		total += 1
		if a.day != 1:
			continue
		dbobj = {
			'pickupTime': a,
			'dropoffTime': datetime.strptime(params[2],'%Y-%m-%d %H:%M:%S'),
			'passengers': int(params[3]),
			'pickupLongitude': float(params[5]),
			'pickupLatitude': float(params[6]),
			'dropoffLongitude': float(params[9]),
			'dropoffLatitude': float(params[10]),
			'fare': float(params[12])
		}
		count += 1
		if count % 10000 == 0:
			print count, total / 10906859.0
		dbobjs.append(dbobj)
	coll.insert_many(dbobjs, ordered = False)

if __name__ == '__main__':
	main()