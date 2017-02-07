import pickle, requests, os

# goes up to 9
SIZ = 9

def main():
	for i in xrange(20, 23):
		fin = 'data/dat{}'.format(i)
		fout = 'data/mat{}'.format(i)
		locs = pickle.load(open(fin, 'r'))
		save = open(fout, 'w')
		st = '{},{}'.format(locs[0]['pickupLatitude'],locs[0]['pickupLongitude'])
		for i in xrange(SIZ):
			st += '|{},{}'.format(locs[i]['dropoffLatitude'],locs[i]['dropoffLongitude'])
		print st
		res = requests.request('GET', 'https://maps.googleapis.com/maps/api/distancematrix/json', params = 
			{
				'origins': st,
				'destinations': st,
				'key': os.environ['API_KEY'],
				'units': 'imperial',
				'departure_time': 1496354400
			})
		rows = res.json()['rows']
		mat = [x[:] for x in [[0] * 10] * 10]
		for i in xrange(SIZ+1):
			for j in xrange(SIZ+1):
				mat[i][j] = rows[i]['elements'][j]['duration']['value']
		for i in xrange(SIZ+1):
			for j in xrange(SIZ+1):
				print '{:5}'.format(mat[i][j]),
			print '\n'
		pickle.dump(mat, save)

if __name__ == '__main__':
	main()