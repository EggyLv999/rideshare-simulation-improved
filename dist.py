import pickle, requests, os

SIZ = 19
CHUNKS = SIZ / 10 + 1

def main():
	for run in xrange(25, 26):
		fin = 'data/dat{}'.format(run)
		fout = 'data/mat{}'.format(run)
		locs = pickle.load(open(fin, 'r'))
		save = open(fout, 'w')
		if len(locs) < SIZ:
			print('abort due to low size')
			return
		sts = ['' for j in xrange(CHUNKS)]
		sts[0] = '|{},{}'.format(locs[0]['pickupLatitude'],locs[0]['pickupLongitude'])
		for i in xrange(SIZ):
			sts[(i+1) / 10] += '|{},{}'.format(locs[i]['dropoffLatitude'],locs[i]['dropoffLongitude'])
		for i in xrange(CHUNKS):
			sts[i] = sts[i][1:]
		rows = [[None] * CHUNKS for i in xrange(CHUNKS)]
		for i in xrange(CHUNKS):
			for j in xrange(CHUNKS):
				res = requests.request('GET',
					'https://maps.googleapis.com/maps/api/distancematrix/json', params = 
					{
						'origins': sts[i],
						'destinations': sts[j],
						'key': os.environ['API_KEY'],
						'units': 'imperial',
						'departure_time': 1496354400
					})
				rows[i][j] = res.json()['rows']
		mat = [x[:] for x in [[0] * (SIZ+1)] * (SIZ+1)]
		for i in xrange(SIZ+1):
			for j in xrange(SIZ+1):
				mat[i][j] = rows[i/10][j/10][i%10]['elements'][j%10]['duration']['value']
		for i in xrange(SIZ+1):
			for j in xrange(SIZ+1):
				print '{:5}'.format(mat[i][j]),
			print '\n'
		pickle.dump(mat, save)

if __name__ == '__main__':
	main()